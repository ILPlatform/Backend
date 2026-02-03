import datetime

def __generate_camp_event(camp_info):
    # Create the Google Event Details
    nl = '\n\n'
    event = {
        'summary': camp_info["summary"],
        'location': camp_info["address"],
        'description': camp_info["description"],
        'start': {
            'dateTime': camp_info["start"],
            'timeZone': 'Europe/Brussels',
        },
        'end': {
            'dateTime': camp_info["end_day1"],
            'timeZone': 'Europe/Brussels',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=5'
        ],
        'attendees': [
            {'email': camp_info["teacher_email"]} if camp_info["teacher_email"] else None,
        ],
        'sendUpdates': 'all'
    }
    return event

def __camp_event(google, sf, camp_info, batch1, batch2, batch3):
    # Generate the Event Details
    event = __generate_camp_event(camp_info)

    # Function to filter the instances to find the excluded days
    excluded_days = camp_info.get("excluded_day").split(",") if camp_info.get("excluded_day") else []
    if camp_info.get("overwrite_cancelled"):
        for day in camp_info.get("overwrite_cancelled").split("\n"):
            excluded_days.append(datetime.datetime.strptime(day, "%d/%m/%Y").strftime("%Y-%m-%d"))
    is_excluded = lambda x: x.get("start").get("dateTime")[:10] in excluded_days

    # Callback for batch request to store event_id and get individual instances
    def callback1(request_id, response, exception):
        if exception:
            print(f'[ERROR] In batch1: {exception}')
        else:
            # Update SF with the Google Event ID
            sf.update_opportunity(camp_info["id"], {"Google_Event__c": response["id"]})

            batch2.add(google.calendar.events().instances(calendarId=google.CALENDAR_CAMPS_ID, eventId=response['id']), callback=callback2)

    # Callback for batch request to delete excluded instances, update first day and update replacements
    def callback2(request_id, response, exception):
        if exception:
            print(f'[ERROR] In batch3: {exception}')
        else:
            # Keep track of first non excluded day
            # first_non_exluded_day = True

            # Loop through the instances (sorted by start date)
            for instance in sorted(response['items'], key=lambda item: item["start"]["dateTime"]):
                updated = False
                if is_excluded(instance):
                    # Delete the excluded instances
                    instance["status"] = "cancelled"
                    updated = True
                # elif first_non_exluded_day:
                #     # Update the start date of the first instance
                #     instance["start"]["dateTime"] = camp_info["start_day1"]
                #     first_non_exluded_day = False
                #     updated = True

                # Find the replacement day, if any
                replacement = next((c for c in camp_info.get("replacements") if c["date"] == instance["start"]["dateTime"][:10]), None)

                # Update the attendees for the replacement day
                if replacement:
                    instance["attendees"] = [{"email": replacement["email"]}]
                    updated = True

                # Update back to original teacher if no replacement but incorrect teacher (so there used to be a replacement but got solved)
                elif instance.get("attendees") and len(instance["attendees"]) > 0 and instance["attendees"][0].get("email") != camp_info["teacher_email"]:
                    instance["attendees"] = [{"email": camp_info["teacher_email"]}]
                    updated = True

                # Only update the instance if it was modified
                if updated:
                    batch3.add(google.calendar.events().update(calendarId=google.CALENDAR_CAMPS_ID, eventId=instance['id'], body=instance, sendUpdates="all"), callback=callback3)

    # Callback for batch request to print final status
    def callback3(request_id, response, exception):
        if exception:
            print(f'[ERROR] In batch3: {exception}')
        else:
            print(f'[INFO] Successfully updated events for {camp_info["code"]}')

    # Update the Opportunity Name if it is different from the Code
    if camp_info.get("code") != camp_info.get("name"):
        sf.sf.Opportunity.update(camp_info["id"], {"Name": camp_info["code"]})

    if not camp_info.get("event_id"):
        # Create the Google Event
        batch1.add(google.calendar.events().insert(calendarId=google.CALENDAR_CAMPS_ID, body=event, sendUpdates="all"), callback=callback1)
    else:
        # Update the Google Event
        batch1.add(google.calendar.events().update(calendarId=google.CALENDAR_CAMPS_ID, eventId=camp_info.get("event_id"), body=event, sendUpdates="all"), callback=callback1)

# def __camp_pictures(google, sf, camp_info):
#     # If holiday specific folder does not exist, create it
#     if camp_info.get("picture_grand_parent_id") == None:
#         created_folder_id = google.create_camp_pictures_folder(f"{camp_info.get('holiday_name')}")
#         sf.sf.Picklist__c.update(camp_info["holiday_id"], {"Google_Drive_Pictures_ID__c": created_folder_id})
#         camp_info["picture_grand_parent_id"] = created_folder_id
#
#     # If week specific folder does not exist, create it
#     if camp_info.get("picture_parent_id") == None:
#         created_folder_id = google.create_camp_pictures_folder(f"{camp_info.get('picture_parent_name')}", parent=camp_info["picture_grand_parent_id"])
#         sf.sf.Picklist__c.update(camp_info["week_id"], {"Google_Drive_Pictures_ID__c": created_folder_id})
#         camp_info["picture_parent_id"] = created_folder_id
#
#     # If camp specific folder does not exist, create it
#     if camp_info["pictures_id"] == None:
#         created_folder_id = google.create_camp_pictures_folder(f"{camp_info.get('pictures_name')}", parent=camp_info["picture_parent_id"])
#         sf.sf.Opportunity.update(camp_info["id"], {"Google_Drive_Pictures__c": created_folder_id})

def update_and_create_camps_per_week(google, sf, week_codes):
    # Get the camp details for the specified weeks
    camps = sf.get_all_camp_details(week_codes)

    # Create Batch Requests
    # batch1: Create or Update the Event
    batch1 = google.calendar.new_batch_http_request()
    # batch2: Get the Instances of the Event
    batch2 = google.calendar.new_batch_http_request()
    # batch3: Delete the Excluded Instances
    batch3 = google.calendar.new_batch_http_request()

    # Create the Events and the Pictures folder for each Camp
    for camp_info in camps:
        try:
            __camp_event(google, sf, camp_info, batch1, batch2, batch3)
            # __camp_pictures(google, sf, camp_info)
            print(f'[SUCCESS] Event created for {camp_info.get("code")}')
        except Exception as e:
            raise ValueError(f'[ERROR] {e}')

    # Execute the Batch Requests
    batch1.execute()
    batch2.execute()
    batch3.execute()

    return "Success", True

def update_and_create_camps(google, sf, camp_id):
    week_code = sf.sf.query(f"SELECT Week__r.Week_Code__c FROM Opportunity WHERE Id = '{camp_id}'")["records"][0]["Week__r"]["Week_Code__c"]
    # Get the camp details for the specified weeks
    camps = [x for x in sf.get_all_camp_details([week_code]) if x["id"] == camp_id]

    # Create Batch Requests
    # batch1: Create or Update the Event
    batch1 = google.calendar.new_batch_http_request()
    # batch2: Get the Instances of the Event
    batch2 = google.calendar.new_batch_http_request()
    # batch3: Delete the Excluded Instances
    batch3 = google.calendar.new_batch_http_request()

    # Create the Events and the Pictures folder for each Camp
    for camp_info in camps:
        try:
            __camp_event(google, sf, camp_info, batch1, batch2, batch3)
            # __camp_pictures(google, sf, camp_info)
            print(f'[SUCCESS] Event created for {camp_info.get("code")}')
        except Exception as e:
            raise ValueError(f'[ERROR] {e}')

    # Execute the Batch Requests
    batch1.execute()
    batch2.execute()
    batch3.execute()

    return "Success", True
