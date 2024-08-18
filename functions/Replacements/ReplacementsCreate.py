import asyncio
from Helpers import firebase_functions_custom, https_fn_custom
from Actions import update_and_create_classes_per_week
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from Salesforce import getSF
from Emails import send_email_admin

import aiohttp
import json

from WhatsApp import send_WA_admins

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def replacements_create(data):
    # Get the parameters
    type = data.get("type")
    class_id = data.get("class_id")
    date = data.get("date")
    teacher_old_id = data.get("teacher_old_id")
    teacher_new_id = data.get("teacher_new_id")
    reason = data.get("reason")
    if not class_id or not date or not type:
        return {"data": {"response": "Class code, type and date are required", "status": 400}}

    # Initialize DB and SF
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

    # Get the teachers name
    teacher_old_name = sf.sf.query(f"SELECT Full_Name__c FROM Employee__c WHERE Id = '{teacher_old_id}'").get("records", [{}])[0].get("Full_Name__c") if teacher_old_id else None
    teacher_new_name = sf.sf.query(f"SELECT Full_Name__c FROM Employee__c WHERE Id = '{teacher_new_id}'").get("records", [{}])[0].get("Full_Name__c") if teacher_new_id else None

    # Retrieve the class information
    class_info = sf.sf.query(f"""
        SELECT
            Account.Name, Code__c,
            Day_of_Week__c,
            Start_Time__c, End_Time__c
        FROM Opportunity
        WHERE Id = '{class_id}'
        """).get("records", [{}])[0]

    # Create a new one time replacement on the given date
    sf.sf.Replacement__c.create({
        "Opportunity__c": class_id,
        "Date__c": date,
        "RecordTypeId": record_type,
        "Teacher_Old__c": teacher_old_id,
        "Teacher__c": teacher_new_id,
        "Reason__c": reason
    })

    # Send email to admins
    send_email_admin(
        subject=f"{type_nice} Replacement {class_info.get('Code__c')}: {teacher_old_name} -> {teacher_new_name}",
        body=f"""
            <p>Dear Admins,</p>
            <p>A replacement has been recorded for the class <b>{class_info.get("Code__c")}</b> on <b>{date}</b>.</p>
            <p>Here are the details regarding the replacement:</p>
            <ul>
                <li><b>School:</b> {class_info.get("Account").get("Name")}</li>
                <li><b>Day:</b> {class_info.get("Day_of_Week__c")}</li>
                <li><b>Time Slot:</b> {class_info.get("Start_Time__c")} - {class_info.get("End_Time__c")}</li>
                <li><b>Replacement Date:</b> {date}</li>
                <li><b>Replacement Type:</b> {type_nice}</li>
                <li><b>Old Teacher:</b> {teacher_old_name}</li>
                <li><b>New Teacher:</b> {teacher_new_name}</li>
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
* *Old Teacher*: {teacher_old_name}
* *New Teacher*: {teacher_new_name}
* *Reason*: {reason}"""))

    return {"data": {"response": "Replacement recorded successfully.", "status": 200}}
