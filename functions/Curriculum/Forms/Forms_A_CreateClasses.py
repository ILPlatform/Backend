from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime, timedelta
from firebase_admin import auth
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def forms_a_create_classes(data):
    # Initialize Google and SF
    sf = getSF()
    google = GoogleConnector()

    # Get and verify the parameters
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    title = data.get("title")
    if not start_date or not end_date or not title:
        return {"data": {"response": "Start and end dates and title are required", "status": 400}}
    try:
        pass
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return {"data": {"response": "Invalid date format", "status": 400}}
    if not start_date <= end_date:
        return {"data": {"response": "End date must be after start date", "status": 400}}

    # Get all classes with start date between the given dates
    classes = sf.sf.query_all_iter(f"""
        SELECT
            Id, Code__c,
            Account.Name, Account.BillingStreet, Account.BillingCity, Account.BillingPostalCode, Account.BillingCountry,
            Day_of_Week__c, Start_Time__c, End_Time__c, Yearly_Schedule__r.Start_Date__c
        FROM Opportunity
        WHERE Yearly_Schedule__r.Start_Date__c >= {start_date}
            AND Yearly_Schedule__r.Start_Date__c <= {end_date}
            AND Teacher__c = null
            AND (StageName = 'Confirmed' OR StageName = 'Awaiting')
            AND RecordTypeId = '012060000003OPWAA2'
        ORDER BY Yearly_Schedule__r.Start_Date__c, Code__c
    """)

    # Process the classes
    processed_classes = [{
        "id": clss.get("Id"),
        "code": clss.get("Code__c"),
        "school": clss.get("Account").get("Name"),
        "address": f"{clss.get('Account').get('BillingStreet')}, {clss.get('Account').get('BillingCity')}, {clss.get('Account').get('BillingPostalCode')}, {clss.get('Account').get('BillingCountry')}",
        "day_of_week": clss.get("Day_of_Week__c"),
        "start_time": clss.get("Start_Time__c"),
        "end_time": clss.get("End_Time__c"),
        "start_date": clss.get("Yearly_Schedule__r").get("Start_Date__c")
    } for clss in classes]

    # Update the start_date to match the correct day_of_week, by selecting the following such day
    for clss in processed_classes:
        start_date = datetime.strptime(clss["start_date"], "%Y-%m-%d")
        while start_date.strftime("%A") != clss["day_of_week"]:
            start_date += timedelta(days=1)
        clss["start_date"] = start_date.strftime("%Y-%m-%d")

    # Group classes by week day
    classes_by_day = {day:
        list(filter(lambda x: x["day_of_week"] == day, processed_classes))
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

    # Generate text for each class
    class_texts = {
        day: list(map(lambda x: f"[{x['code']}] {x['school']} ({x['address']}) à partir du {x['start_date']} - {x['start_time'][:5] if x.get('start_time') else '??'}-{x['end_time'][:5] if x.get('end_time') else '??'}", classes_by_day[day]))
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

    # Filter out days with no classes
    class_texts = {day: class_texts[day] for day in class_texts if len(class_texts[day])}

    # Lambda function to translate day of week to French
    translate_day = lambda day: {
        "Monday": "Lundi",
        "Tuesday": "Mardi",
        "Wednesday": "Mercredi",
        "Thursday": "Jeudi",
        "Friday": "Vendredi",
        "Saturday": "Samedi",
        "Sunday": "Dimanche"
    }[day]

    # Create Google Form
    body = {"addParents": ["1llQJfvK-FNlQ26-9HmUXWKALy59cr8uM"]}
    form = google.drive.files().copy(fileId=google.CLASSES_FORM_ID, body=body).execute()

    # Generate update request
    update = {
        "requests": [
            {
                "createItem": {
                    "item": {
                        "title": translate_day(day),
                        "questionItem": {
                            "question": {
                                "choiceQuestion": {
                                    "type": "CHECKBOX",
                                    "options": [
                                        {"value": class_text} for class_text in class_texts[day]
                                    ]
                                }
                            }
                        },
                    },
                    "location": {"index": 5 + i},
                }
            }
        for i, day in enumerate(class_texts.keys())
        ]
    }
    update["requests"].append({
        "updateFormInfo": {
            "info": {"title": title},
            "updateMask": "title",
        }
    })

    # Update Form
    result = google.forms.forms().batchUpdate(formId=form['id'], body=update).execute()

    # Get Form
    form = google.forms.forms().get(formId=form['id']).execute()

    return {"data": {"response": form['responderUri'], "status": 200}}
