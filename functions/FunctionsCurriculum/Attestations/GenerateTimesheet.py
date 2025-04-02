from Google import TimesheetDocument
from Emails import send_email_user

def generate_timesheet(google, sf, teacher, year, month):
    # Generate Timesheet Document
    Timesheet = TimesheetDocument(google, teacher, year, month)
    Timesheet.fill()
    teacher.update({"link": Timesheet.get_download_link()})

    # Add the document to Salesforce
    document = sf.sf.Document__c.create({
        "Year__c": year,
        "Month__c": month,
        "Teacher__c": teacher.get("id"),
        "Type__c": "Attestation",
        "Description__c": f"Attestation - {year}/{month}",
        "Unsigned_URL__c": teacher.get("link"),
        "RecordTypeId": "012P5000001T8MbIAK",
        "To_Sign__c": True,
    })

    # Add the payment to SF
    sf.sf.Payment__c.create({
      "Document__c": document.get("id"),
      "Year__c": year,
      "Month__c": month,
      "Paid__c": False,
      "Beneficiary__c": teacher.get("id"),
      "Type_of_Payment__c": teacher.get("Contract_Type__c"),
      "Contract__c": "contract" in teacher.get("Contract_Type__c").lower(),
      "Amount__c": teacher.get('total_amount'),
      "RecordTypeId": "012P5000001tRevIAE",
    })

    # Send email to the user
    send_email_user(teacher.get("email"),
        "Nouveau Document Disponible",
        f"""
        <p>
            Bonjour {teacher.get("name")},
        </p>
        <p>
            Un nouveau document ({f"Attestation - {year}/{month}"}) est disponible pour toi. Tu peux le retrouver sur le <a href="https://curriculum.ilplatform.be">site curriculum</a>, sous "My Account" > "Documents", ou en pièce jointe à cet email. Si le document en question requiert une signature, merci de le signer via le site curriculum.
        </p>
        <p>
            Merci de ne pas répondre à cet email. Si tu as des questions, merci de nous contacter via WhatsApp ou via <a href="mailto:daniel@ilplatform.be">daniel@ilplatform.be</a>.
        </p>
        <p>
            Merci et bien à toi,
        </p>
        """,
        file_url=teacher.get("link"),
        file_name=f"Attestation - {year}/{month}")
