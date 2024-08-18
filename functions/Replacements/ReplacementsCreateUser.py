import asyncio
from Helpers import firebase_functions_custom, https_fn_custom
from Actions import update_and_create_classes_per_week
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from Salesforce import getSF

from Emails import send_email_admin, send_email_user
from WhatsApp import send_WA_admins

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def replacements_create_user(data):
    # Get the parameters
    uid = data.get("uid")
    type = data.get("type")
    class_id = data.get("class_id")
    date = data.get("date")
    reason = data.get("reason")
    if not uid or not type or not class_id or not date or not reason:
        return {"data": {"response": "All fields are required", "status": 400}}

    # Initialize SF
    sf = getSF()

    # Get the day of the class
    day = sf.sf.query(f"SELECT Day_of_Week__c FROM Opportunity WHERE Id = '{class_id}'").get("records", [{}])[0].get("Day_of_Week__c")

    # Ensure the indicated date coincides with a class date
    if not datetime.strptime(date, "%Y-%m-%d").strftime("%A") == day:
        return {"data": {"response": f"The indicated date does not coincide with the class day of {day}", "status": 400}}

    # Determine Record Type
    if type == "permanent":
        record_type = "012P5000001QAUbIAO"
        type_nice = "Permanent"
    elif type == "one-time":
        record_type = "012P5000001QASzIAO"
        type_nice = "One-Time"
    else:
        return {"data": {"response": "Invalid type", "status": 400}}

    # Retrieve the teacher id
    teacher_info = sf.sf.query(f"""
        SELECT Id, Name, Full_Name__c, Email__c FROM Employee__c
        WHERE Firebase_UID__c = '{uid}'
    """).get("records", [{}])[0]

    # Retrieve the class information
    class_info = sf.sf.query(f"""
        SELECT
            Account.Name, Code__c,
            Day_of_Week__c,
            Start_Time__c, End_Time__c
        FROM Opportunity
        WHERE Id = '{class_id}'
        """).get("records", [{}])[0]

    # Create a new replacement on the given date
    sf.sf.Replacement__c.create({
        "Opportunity__c": class_id,
        "Date__c": date,
        "RecordTypeId": record_type,
        "Teacher_Old__c": teacher_info.get("Id"),
        "Reason__c": reason
    })

    # Send email to teacher
    send_email_user(
        email=teacher_info.get("Email__c"),
        subject=f"{type_nice} Replacement Request {class_info.get('Code__c')}: {teacher_info.get('Name')}",
        body=f"""
            <p>Dear {teacher_info.get("Name")},</p>
            <p>Your replacement request has been recorded for the class <b>{class_info.get("Code__c")}</b> on <b>{date}</b>.</p>
            <p>Here are the details regarding the replacement:</p>
            <ul>
                <li><b>School:</b> {class_info.get("Account").get("Name")}</li>
                <li><b>Day:</b> {class_info.get("Day_of_Week__c")}</li>
                <li><b>Time Slot:</b> {class_info.get("Start_Time__c")} - {class_info.get("End_Time__c")}</li>
                <li><b>Replacement Date:</b> {date}</li>
                <li><b>Replacement Type:</b> {type_nice}</li>
                <li><b>Old Teacher:</b> {teacher_info.get("Name")}</li>
                <li><b>Reason:</b> {reason}</li>
            </ul>
            <p>
                Kind regards, <br>
            </p>
        """
    )

    # Send email to admins
    send_email_admin(
        subject=f"{type.upper()} Replacement {class_info.get('Code__c')}: {teacher_info.get('Name')}",
        body=f"""
            <p>Dear Admins,</p>
            <p>A <b>{type_nice}</b> replacement has been recorded for the class <b>{class_info.get("Code__c")}</b> on <b>{date}</b>.</p>
            <p>Here are the details regarding the replacement:</p>
            <ul>
                <li><b>School:</b> {class_info.get("Account").get("Name")}</li>
                <li><b>Day:</b> {class_info.get("Day_of_Week__c")}</li>
                <li><b>Time Slot:</b> {class_info.get("Start_Time__c")} - {class_info.get("End_Time__c")}</li>
                <li><b>Replacement Date:</b> {date}</li>
                <li><b>Replacement Type:</b> {type_nice}</li>
                <li><b>Old Teacher:</b> {teacher_info.get("Full_Name__c")}</li>
                <li><b>New Teacher:</b> </li>
                <li><b>Reason:</b> {reason}</li>
            </ul>
            <p>
                Kind regards, <br>
            </p>
        """
    )

    # Send WhatsApp message
    asyncio.run(send_WA_admins(f"""Hello! A new {type_nice} replacement request has been made.
* *School*: {class_info.get("Account").get("Name")}
* *Day*: {class_info.get("Day_of_Week__c")}
* *Time Slot*: {class_info.get("Start_Time__c")[:5] if class_info.get("Start_Time__c") else "??"} - {class_info.get("End_Time__c")[:5] if class_info.get("End_Time__c") else "??"}
* *Replacement Date*: {date}
* *Replacement Type*: {type_nice}
* *Old Teacher*: {teacher_info.get("Full_Name__c")}
* *New Teacher*:
* *Reason*: {reason}"""))

    return {"data": {"response": "Replacement recorded successfully.", "status": 200}}
