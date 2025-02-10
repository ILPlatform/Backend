from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
import datetime
from Salesforce import getSF

from .getSchedule import getSchedule

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def events_u_update_class(data):
    # Initialize Google and SF
    sf = getSF()
    google = GoogleConnector()

    # Retrieve class ID
    class_id = data.get('class_id')
    if not class_id:
        return {"data": {"response": "Missing class_id", "status": 400}}

    # Retrieve class data with all replacements
    class_data = sf.sf.query(f"""
        SELECT
            Id, Name, Code__c, Teacher__r.Email__c, Teacher__r.Full_Name__c,
            Account.Name, Account.BillingAddress, Account.Online__c,
            Start_Time__c, End_Time__c, Day_of_Week__c,
            Yearly_Schedule__r.Start_Date__c, Yearly_Schedule__r.End_Date__c,
            Yearly_Schedule__r.Associated_Calendar__r.Holiday_Weeks__c, Yearly_Schedule__r.Associated_Calendar__r.Holiday_Days__c,
            Yearly_Schedule__r.Overwrite_Cancelled__c,
            Yearly_Schedule__r.Attendance_Description__c,
            Overwrite_Cancelled__c, Additional_Invite__c,
            Google_Event__c, Ages_Announced__c,
            (
                SELECT
                    Teacher__r.Email__c, Teacher__r.Full_Name__c,
                    Date__c, RecordTypeId
                FROM Replacements__r
                WHERE Deleted__c = False
            )
        FROM Opportunity
        WHERE Id = '{class_id}'
    """)

    # Check if class exists
    if not class_data['records']:
        return {"data": {"response": "Class not found", "status": 404}}

    # Retrieve class data
    class_data = class_data['records'][0]

    teacher_schedule_one_time = getSchedule(class_data)
    course_days = list(teacher_schedule_one_time.keys())

    ## Step 5: Generate the Google Calendar events
    # Create Batch Requests
    # batch1: Create or Update the Event
    batch1 = google.calendar.new_batch_http_request()
    # batch2: Get the Instances of the Event
    batch2 = google.calendar.new_batch_http_request()
    # batch3: Delete the Excluded Instances
    batch3 = google.calendar.new_batch_http_request()

    # Callback for batch request to store event_id and get individual instances
    def callback1(request_id, response, exception):
        if exception:
            print(f'[ERROR] In batch1: {exception}')
        else:
            sf.sf.Opportunity.update(class_data["Id"], {"Google_Event__c": response["id"]})

            batch2.add(google.calendar.events().instances(calendarId=google.CALENDAR_CLASSES_ID, eventId=response['id']), callback=callback2)

    # Callback for batch request to delete excluded instances, update first day and update replacements
    def callback2(request_id, response, exception):
        if exception:
            print(f'[ERROR] In batch3: {exception}')
        else:
            # Loop through the instances (sorted by start date)
            firstAllUpdate = True
            for instance in sorted(response['items'], key=lambda item: item["start"]["dateTime"]):
                instance_date = datetime.datetime.strptime(instance["start"]["dateTime"][:10], '%Y-%m-%d').date()

                # Check if the date should be held
                if instance_date not in course_days:
                    print("SHOULD BE CANCELLED")
                    instance["status"] = "cancelled"
                    batch3.add(google.calendar.events().update(calendarId=google.CALENDAR_CLASSES_ID, eventId=instance['id'], body=instance, sendUpdates="none"), callback=callback3)

                # Check if the attendees should be updated
                elif set((map(lambda x: x["email"], teacher_schedule_one_time.get(instance_date, [])))) != set(list(map(lambda x: x.get("email"), instance.get("attendees", [])))):
                    instance["attendees"] = [
                        {"email": teacher["email"]}
                        for teacher
                        in teacher_schedule_one_time.get(instance_date, [])]

                    # Determine whether to send updates or not
                    sendUpdates = "all"
                    previous_index = course_days.index(instance_date) - 1
                    if previous_index >= 0:
                        previous_attendees = teacher_schedule_one_time.get(course_days[previous_index])
                        if previous_attendees != teacher_schedule_one_time.get(instance_date):
                            sendUpdates = "none"

                    batch3.add(google.calendar.events().update(calendarId=google.CALENDAR_CLASSES_ID, eventId=instance['id'], body=instance, sendUpdates=sendUpdates), callback=callback3)

    # Callback for batch request to print final status
    def callback3(request_id, response, exception):
        if exception:
            print(f'[ERROR] In batch3: {exception}')
        else:
            print(f'[INFO] Successfully updated events for {class_data["Code__c"]}')

    # Define the event details
    start_date = course_days[0]
    start_time = datetime.datetime.strptime(class_data["Start_Time__c"][:-1], "%H:%M:%S.%f").time()
    end_time = datetime.datetime.strptime(class_data["End_Time__c"][:-1], "%H:%M:%S.%f").time()
    start_datetime = datetime.datetime.combine(start_date, start_time)
    if not class_data["Account"]["Online__c"]:
        start_datetime -= datetime.timedelta(minutes=15)
    start_datetime_iso = start_datetime.isoformat()
    end_datetime = datetime.datetime.combine(start_date, end_time) # + datetime.timedelta(minutes=15)
    end_datetime_iso = end_datetime.isoformat()
    event = {
        'summary': f'{class_data["Code__c"]} - {class_data["Account"]["Name"]} [{class_data["Ages_Announced__c"] if class_data.get("Ages_Announced__c") and class_data.get("Ages_Announced__c") != "" else "???"}]',
        'location': f'{class_data["Account"]["BillingAddress"]["street"]}, {class_data["Account"]["BillingAddress"]["postalCode"]} {class_data["Account"]["BillingAddress"]["city"]}, {class_data["Account"]["BillingAddress"]["country"]}',
        'description':
            f"Horaire de cours: {class_data['Start_Time__c'][:5]} - {class_data['End_Time__c'][:5]}. Arrivée attendue 15 minutes avant pour préparer la salle.\n\n" + \
            f"Procédure de présences: {class_data['Yearly_Schedule__r']['Attendance_Description__c']}",
        'start': {
            'dateTime': start_datetime_iso,
            'timeZone': 'Europe/Brussels',
        },
        'end': {
            'dateTime': end_datetime_iso,
            'timeZone': 'Europe/Brussels',
        },
        'recurrence': [
            f'RRULE:FREQ=WEEKLY;UNTIL={class_data["Yearly_Schedule__r"]["End_Date__c"].replace("-", "")}T235959Z'
        ],
        'attendees': [
            {'email': class_data["Teacher__r"]["Email__c"]} if class_data.get("Teacher__r") else None,
            {'email': class_data["Additional_Invite__c"]} if class_data.get("Additional_Invite__c") else None
        ],
        "conferenceData": {
            "createRequest": {
                "conferenceSolutionKey": {
                "type": "hangoutsMeet"
                },
                "requestId": f'{class_data["Code__c"]} - {class_data["Account"]["Name"]} [{class_data["Ages_Announced__c"] if class_data.get("Ages_Announced__c") and class_data.get("Ages_Announced__c") != "" else "???"}]',
            }
        } if class_data["Account"]["Online__c"] else None,
        'sendUpdates': 'all'
    }
    print(event)

    if not class_data.get("Google_Event__c"):
        # Create the Google Event
        batch1.add(google.calendar.events().insert(calendarId=google.CALENDAR_CLASSES_ID, body=event, sendUpdates="all", conferenceDataVersion=1), callback=callback1)
    else:
        # Update the Google Event
        batch1.add(google.calendar.events().update(calendarId=google.CALENDAR_CLASSES_ID, eventId=class_data["Google_Event__c"], body=event, sendUpdates="none", conferenceDataVersion=1), callback=callback1)

    # Execute the Batch Requests
    batch1.execute()
    batch2.execute()
    batch3.execute()

    # Dummy return
    return {"data": {"response": "Success", "status": 200}}
