from Emails import send_email_user
from Google import GoogleConnector, PayslipA17Document
from Helpers import firebase_functions_custom, https_fn_custom, safe_create
from Salesforce import getSF


def _get_value(data, key, sf_key=None):
    details = data.get("details") or {}
    return data.get(key) or details.get(key) or (details.get(sf_key) if sf_key else None)


def _parse_month_year(data):
    month_value = _get_value(data, "month", "Month__c")
    year_value = _get_value(data, "year", "Year__c")

    if isinstance(month_value, str) and "-" in month_value and not year_value:
        year_part, month_part = month_value.split("-", 1)
        year_value = year_part
        month_value = month_part

    month = int(month_value)
    year = int(year_value)

    if month < 1 or month > 12:
        raise ValueError("month must be between 1 and 12")

    return month, year


def _format_teacher_details(record):
    nn = (record.get("Registration_Number__c") or "").replace(".", "")

    return record | {
        "id": record.get("Id"),
        "name": record.get("Full_Name__c"),
        "email": record.get("Email__c"),
        "address": f'{record.get("Address__Street__s")}, {record.get("Address__PostalCode__s")} {record.get("Address__City__s")}',
        "iban": record.get("IBAN__c"),
        "bic": record.get("BIC__c"),
        "nn": record.get("Registration_Number__c"),
        "birthdate": f"{nn[4:6]}/{nn[2:4]}/{nn[0:2]}" if len(nn) >= 6 else None,
    }


@https_fn_custom()
@firebase_functions_custom(auth_level=3)
def docs_a_create_payslip_a17(data):
    sf = getSF()
    google = GoogleConnector()

    teacher_id = _get_value(data, "teacher_id", "Teacher__c")
    if not teacher_id:
        raise ValueError("Missing teacher_id")

    month, year = _parse_month_year(data)

    teacher_records = sf.sf.query(f"""
        SELECT Id, Full_Name__c, Email__c, Address__Street__s, Address__City__s,
            Address__PostalCode__s, IBAN__c, BIC__c, Registration_Number__c
        FROM Employee__c
        WHERE Id='{teacher_id}'
        LIMIT 1
    """).get("records", [])

    if len(teacher_records) == 0:
        raise ValueError(f"Teacher {teacher_id} not found")

    teacher = _format_teacher_details(teacher_records[0])

    payment_records = sf.sf.query(f"""
        SELECT Id, Amount__c, Month__c, Year__c, CreatedDate
        FROM Payment__c
        WHERE Beneficiary__c='{teacher_id}'
            AND Month__c={month}
            AND Year__c={year}
            AND RecordTypeId='012P5000001tRevIAE'
            AND Deleted__c=False
        ORDER BY CreatedDate DESC
        LIMIT 1
    """).get("records", [])

    if len(payment_records) == 0:
        raise ValueError(f"No payment found for teacher {teacher_id} in {year}-{month:02d}")

    payment = payment_records[0]

    payslip = PayslipA17Document(google, teacher, payment, year, month)
    payslip.fill()
    link = payslip.get_download_link()
    if not link:
        raise ValueError("Could not generate Payslip A17 download link")

    description = f"Payslip A17 - {year}/{month:02d}"
    details = {
        "RecordTypeId": "012P5000001T9P7IAK",
        "Teacher__c": teacher_id,
        "Description__c": description,
        "Unsigned_URL__c": link,
        "To_Sign__c": False,
    }

    document = safe_create(sf.sf.Document__c, details)

    send_email_user(
        teacher.get("email"),
        "Nouveau Document Disponible",
        f"""
        <p>
            Bonjour {teacher.get("name")},
        </p>
        <p>
            Un nouveau document ({description}) est disponible pour toi. Tu peux le retrouver sur le <a href="https://curriculum.ilplatform.be">site curriculum</a>, sous "My Account" > "Documents", ou en pièce
            jointe à cet email.
        </p>
        <p>
            Merci de ne pas répondre à cet email. Si tu as des questions, merci de nous contacter via WhatsApp ou via <a href="mailto:daniel@ilplatform.be">daniel@ilplatform.be</a>.
        </p>
        <p>
            Merci et bien à toi,
        </p>
        """,
        file_url=link,
        file_name=description,
    )

    return {"data": {"response": {
        "Id": document.get("id"),
        "Unsigned_URL__c": link,
        "Payment__c": payment.get("Id"),
    }, "status": 200}}
