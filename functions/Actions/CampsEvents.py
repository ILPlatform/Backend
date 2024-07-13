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

def create_camp_event(google_calendar, sf, camp_code):
    # Get the Camp Details
    camp_info = sf.get_camp_details(camp_code)

    # Check if the Event already exists
    if camp_info["event_id"] != None:
        print(f'[WARNING] Event already created for {camp_info["code"]}')
        return False

    # Generate the Event Details
    event = __generate_camp_event(camp_info)

    # Create the Google Event
    created_event = google_calendar.create_event(event)

    # Update the Salesforce Opportunity with the Google Event ID
    sf.update_opportunity(camp_info["id"], {"Google_Event__c": created_event["id"]})

    return True

def create_camp_pictures(google, sf, camp_code):
    # Get the Camp Details
    camp_info = sf.get_camp_details(camp_code)

    if camp_info.get("picture_grand_parent_id") == None:
        created_folder_id = google.create_camp_pictures_folder(f"{camp_info.get('holiday_name')}")
        sf.update_picklist(camp_info["holiday_id"], {"Google_Drive_Pictures_ID__c": created_folder_id})
        camp_info["picture_grand_parent_id"] = created_folder_id

    if camp_info.get("picture_parent_id") == None:
        created_folder_id = google.create_camp_pictures_folder(f"{camp_info.get('picture_parent_name')}", parent=camp_info["picture_grand_parent_id"])
        sf.update_picklist(camp_info["week_id"], {"Google_Drive_Pictures_ID__c": created_folder_id})
        camp_info["picture_parent_id"] = created_folder_id
    else:
        google.update_camp_pictures_folder(camp_info["picture_parent_id"], camp_info["picture_parent_name"], parent=camp_info["picture_grand_parent_id"])

    if camp_info["pictures_id"] == None:
        # Create the Google Folder
        created_folder_id = google.create_camp_pictures_folder(f"{camp_info.get('pictures_name')}", parent=camp_info["picture_parent_id"])

        # Update the Salesforce Opportunity with the Google Event ID
        sf.update_opportunity(camp_info["id"], {"Google_Drive_Pictures__c": created_folder_id})
    else:
        google.update_camp_pictures_folder(camp_info["pictures_id"], camp_info["pictures_name"], parent=camp_info["picture_parent_id"])

def update_camp_event(google_calendar, sf, camp_code):
    # Get the Camp Details
    camp_info = sf.get_camp_details(camp_code)

    # Check if the Event already exists
    if camp_info["event_id"] == None:
        print(f'[WARNING] Event for {camp_info["code"]} does not yet exist and hence cannot be updated')
        return False

    # Generate the Event Details
    event = __generate_camp_event(camp_info)

    # Update the Google Event
    google_calendar.update_event(camp_info["event_id"], event)

    return True

def update_and_create_camps_per_week(google, sf, week_codes):
    # Get the Camp Codes for the Week
    camp_codes = []
    for week_code in week_codes:
        camp_codes += sf.get_camps_per_week(week_code, True)
    print(f'[INFO] Found {len(camp_codes)} Camps for {week_codes}, namely {", ".join(camp_codes)}')

    # Create the Events for each Camp
    for camp_code in camp_codes:
        try:
            if create_camp_event(google, sf, camp_code):
                print(f'[SUCCESS] Event created for {camp_code}')
            else:
                update_camp_event(google, sf, camp_code)
                print(f'[SUCCESS] Event updated for {camp_code}')

            # Create the Google Drive Folder for the Camp Pictures
            create_camp_pictures(google, sf, camp_code)
        except Exception as e:
            raise ValueError(f'[ERROR] {e}')

    return "Success", True
