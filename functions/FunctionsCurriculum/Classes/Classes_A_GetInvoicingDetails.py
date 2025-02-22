from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF
from ..Events import getSchedule

@https_fn_custom()
@firebase_functions_custom(auth_level=5)
def classes_a_get_invoicing_details(data):
    # Retrieve data
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    organisation_name = data.get("organisation_name")
    with_regs = data.get("with_regs")

    # Initialize DB and SF
    sf = getSF()

    # Get the user
    result = sf.sf.query_all_iter(f"""
        SELECT
            Id, Code__c, Day_of_Week__c, Start_Time__c, End_Time__c,
            Account.Short_Name__c, Account.BillingAddress, Account.Online__c,
            Yearly_Schedule__r.Start_Date__c, Yearly_Schedule__r.End_Date__c,
            Teacher__r.Full_Name__c, Teacher__r.Email__c,
            Teacher__r.Id, Teacher__r.Firebase_UID__c,
            Google_Event__c, Additional_Invite__c,
            Yearly_Schedule__r.Associated_Calendar__r.Holiday_Weeks__c,
            Yearly_Schedule__r.Associated_Calendar__r.Holiday_Days__c,
            Yearly_Schedule__r.Overwrite_Cancelled__c,
            Overwrite_Cancelled__c, Registrations__c,
            (
                SELECT
                    RecordTypeId, Date__c,
                    Teacher__r.Full_Name__c, Teacher__r.Email__c,
                    Teacher__r.Id, Teacher__r.Firebase_UID__c
                FROM Replacements__r
                WHERE Deleted__c = False AND RecordTypeId = '012P5000001QAUbIAO'
            )
        FROM Opportunity
        WHERE RecordTypeId = '012060000003OPWAA2'
            AND StageName!='Cancelled'
            AND Partner_Organisation__c LIKE '%{organisation_name}%'
    """)

    # Function to translate date in format YYYY-MM-DD to DD/MM
    def translate_date(date):
        MM = date[5:7]
        DD = date[8:10]
        return f"{DD}/{MM}"

    # Process the result
    codes = [{
        "id": code.get("Id"),
        "code": code.get("Code__c"),
        "day_of_week": code.get("Day_of_Week__c"),
        "time": f"{code.get('Start_Time__c')[:5] if code.get('Start_Time__c') else '??'}-{code.get('End_Time__c')[:5] if code.get('End_Time__c') else '??'}",
        "school_name": code.get("Account").get("Short_Name__c") if code.get("Account") else None,
        "classes": ", ".join([translate_date(str(k)) for (k, v) in getSchedule(code).items() if start_date <= str(k) <= end_date]),
        "number_classes": len([1 for (k, v) in getSchedule(code).items() if start_date <= str(k) <= end_date]),
        "registrations": int(code.get("Registrations__c")) if with_regs else 0,
    } for code in result]
    codes.sort(key=lambda x: x["code"])

    # Function to translate English day of week to French
    def translate_day(day):
        return {
            "Monday": "Lundi",
            "Tuesday": "Mardi",
            "Wednesday": "Mercredi",
            "Thursday": "Jeudi",
            "Friday": "Vendredi",
            "Saturday": "Samedi",
            "Sunday": "Dimanche"
        }.get(day, day)

    # Process again
    if with_regs:
        descriptions = [
            f'{c["school_name"]} ({translate_day(c["day_of_week"])} {c["time"]}) -> {c["number_classes"]} cours ({c["classes"]}) à {c["registrations"]} inscrits => {int(c["registrations"] * c["number_classes"])}' for c in codes
        ]
        total = sum([int(c["registrations"] * c["number_classes"]) for c in codes])
    else:
        descriptions = [
            f'{c["school_name"]} ({translate_day(c["day_of_week"])} {c["time"]}) -> {c["number_classes"]} cours ({c["classes"]})' for c in codes
        ]
        total = sum([c["number_classes"] for c in codes])

    return {"data": {"response": {"descriptions": descriptions, "total": total}, "status": 200}}
