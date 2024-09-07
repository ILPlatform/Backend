from pprint import pprint
from datetime import datetime, timedelta

def get_nearest_day_datetime_iso(start_date_str, day_name, time_str, direction="after"):
    # Mapping of day names to weekday numbers
    days_of_week = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6
    }

    # Convert the input date and time to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    target_day_num = days_of_week[day_name]

    # Get the weekday number of the start date
    start_day_num = start_date.weekday()

    # Determine the number of days to add or subtract based on the direction
    if direction == "after":
        days_until_next = (target_day_num - start_day_num) % 7
        if days_until_next == 0:
            nearest_day_date = start_date
        else:
            nearest_day_date = start_date + timedelta(days=days_until_next)
    elif direction == "before":
        days_until_previous = (start_day_num - target_day_num) % 7
        if days_until_previous == 0:
            nearest_day_date = start_date
        else:
            nearest_day_date = start_date - timedelta(days=days_until_previous)
    else:
        raise ValueError("Direction should be either 'after' or 'before'")

    # Add the time to the nearest_day_date, allowing for optional seconds and milliseconds
    time_formats = ["%H:%M:%S.%f", "%H:%M:%S", "%H:%M"]

    for fmt in time_formats:
        try:
            time_parts = datetime.strptime(time_str, fmt).time()
            break
        except ValueError:
            continue
    else:
        raise ValueError("Time format is incorrect")

    # Combine date and time
    nearest_day_datetime = datetime.combine(nearest_day_date, time_parts)

    # Return the datetime in ISO 8601 format with the specified timezone offset
    iso_format_str = nearest_day_datetime.isoformat() + "+02:00"

    return iso_format_str

def generate_date_list_from_intervals(intervals):
    all_dates = []

    for interval in intervals:
        # Split each interval into start and end dates
        start_str, end_str = interval.split(" - ")

        # Convert the start and end dates to datetime objects
        start_date = datetime.strptime(start_str, "%d/%m/%Y")
        end_date = datetime.strptime(end_str, "%d/%m/%Y")

        # Generate all dates within the interval
        current_date = start_date
        while current_date <= end_date:
            all_dates.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)

    return all_dates

def __generate_class_event(class_info):
    # Create the Google Event Details
    nl = '\n\n'
    event = {
        'summary': class_info["event"]["summary"],
        'location': class_info["event"]["address"],
        'description': "",
        'start': {
            'dateTime': get_nearest_day_datetime_iso(class_info["event"]["start_date"], class_info["event"]["day"] ,class_info["event"]["start_time"], "after"),
            'timeZone': 'Europe/Brussels',
        },
        'end': {
            'dateTime': get_nearest_day_datetime_iso(class_info["event"]["start_date"], class_info["event"]["day"] ,class_info["event"]["end_time"], "after"),
            'timeZone': 'Europe/Brussels',
        },
        'recurrence': [
            f'RRULE:FREQ=WEEKLY;UNTIL={class_info["event"]["end_date"].replace("-", "")}T235959Z'
        ],
        'attendees': [
            {'email': class_info["event"]["email"]} if class_info["event"]["email"] else None,
            {'email': class_info["event"]["additional_invite"]} if class_info["event"]["additional_invite"] else None,
        ],
        "conferenceData": {
            "createRequest": {
                "conferenceSolutionKey": {
                "type": "hangoutsMeet"
                },
                "requestId": class_info["event"]["summary"]
            }
        } if class_info["event"]["online"] else None,
        'sendUpdates': 'all'
    }
    return event

def __class_event(google, sf, class_info, batch1, batch2, batch3):
    # Generate the Event Details
    event = __generate_class_event(class_info)
    weeks = class_info.get("holidays").get("weeks").splitlines() if class_info.get("holidays").get("weeks") else []
    days = list(map(lambda d: datetime.strptime(d, "%d/%m/%Y").strftime("%Y-%m-%d"), class_info.get("holidays").get("days").splitlines() if class_info.get("holidays").get("days") else []))
    days_oc_ys = list(map(lambda d: datetime.strptime(d, "%d/%m/%Y").strftime("%Y-%m-%d"), class_info.get("holidays").get("overwrite_cancelled_ys").splitlines() if class_info.get("holidays").get("overwrite_cancelled_ys") else []))
    days_oc = list(map(lambda d: datetime.strptime(d, "%d/%m/%Y").strftime("%Y-%m-%d"), class_info.get("holidays").get("overwrite_cancelled").splitlines() if class_info.get("holidays").get("overwrite_cancelled") else []))
    holiday_weeks = generate_date_list_from_intervals(weeks)
    is_holiday = lambda instance: instance["start"]["dateTime"][:10] in holiday_weeks or instance["start"]["dateTime"][:10] in days or instance["start"]["dateTime"][:10] in days_oc_ys or instance["start"]["dateTime"][:10] in days_oc

    # Callback for batch request to store event_id and get individual instances
    def callback1(request_id, response, exception):
        if exception:
            print(f'[ERROR] In batch1: {exception}')
        else:
            # print(response['id'])
            # Update SF with the Google Event ID
            sf.sf.Opportunity.update(class_info["id"], {"Google_Event__c": response["id"]})

            batch2.add(google.calendar.events().instances(calendarId=google.CALENDAR_CLASSES_ID, eventId=response['id']), callback=callback2)

    # Callback for batch request to delete excluded instances, update first day and update replacements
    def callback2(request_id, response, exception):
        if exception:
            print(f'[ERROR] In batch3: {exception}')
        else:
            # The main email address
            permenant_email = class_info.get("event").get("email")

            # Get permanent replacements
            permenant_replacements = sorted(class_info.get("replacements").get("permanent") or [], key=lambda item: item["date"])

            # Loop through the instances (sorted by start date)
            firstAllUpdate = True
            for instance in sorted(response['items'], key=lambda item: item["start"]["dateTime"]):
                updated = False
                sendUpdates = "none"

                # If the additional invite exists and is not in the instance, add it
                if class_info.get("event").get("additional_invite") and not any(attendee["email"] == class_info.get("event").get("additional_invite") for attendee in instance["attendees"]):
                    instance["attendees"].append({'email': class_info.get("event").get("additional_invite")})
                    sendUpdates = "all"
                    updated = True

                # Check if the date falls in a holidays week
                if is_holiday(instance):
                    instance["status"] = "cancelled"
                    sendUpdates = "none"
                    updated = True

                # Find the permanent replacement day, if any
                # replacements_permanant = class_info.get("replacements").get("permanent") or []
                # replacement_permanent = next((c for c in replacements_permanant if c["date"] == instance["start"]["dateTime"][:10]), None)

                # Update the attendees for the permanent replacement day
                if len(permenant_replacements) > 0 and permenant_replacements[0]["date"] <= instance["start"]["dateTime"][:10]:
                    permenant_email = permenant_replacements[0]["email"]
                    permenant_replacements = permenant_replacements[1:]
                    firstAllUpdate = True

                # Find the one-time replacement day, if any
                replacements_one_time = class_info.get("replacements").get("one_time") or []
                replacement_one_time = next((c for c in replacements_one_time if c["date"] == instance["start"]["dateTime"][:10]), None)

                # Find the instance_email
                instance_email = instance["attendees"][0]["email"] if instance.get("attendees") and len(instance["attendees"]) > 0 and instance["attendees"][0].get("email") else None

                # Update the attendees for the one-time replacement day
                if replacement_one_time:
                    sendUpdates = "all"
                    if (not instance.get("attendees") or (instance.get("attendees") and len(instance.get("attendees")) == 0)) and replacement_one_time["email"]:
                        instance["attendees"] = [
                            {"email": replacement_one_time["email"]},
                            {'email': class_info.get("event").get("additional_invite")} if class_info.get("event").get("additional_invite") else None,
                        ]
                        updated = True
                    elif instance.get("attendees") and len(instance["attendees"]) > 0 and instance["attendees"][0].get("email") != replacement_one_time["email"]:
                        if replacement_one_time["email"]:
                            instance["attendees"] = [
                                {"email": replacement_one_time["email"]},
                                {'email': class_info.get("event").get("additional_invite")} if class_info.get("event").get("additional_invite") else None,
                            ]
                        else:
                            instance["attendees"] = [
                                {'email': class_info.get("event").get("additional_invite")},
                            ]  if class_info.get("event").get("additional_invite") else []
                        updated = True
                else:
                    # If there is no one-time replacement and there is no current teacher, mark the permanent teacher as the teacher
                    if (not instance.get("attendees") or (instance.get("attendees") and len(instance.get("attendees")) == 0)):
                        if permenant_email:
                            instance["attendees"] = [
                                {"email": permenant_email},
                                {'email': class_info.get("event").get("additional_invite")} if class_info.get("event").get("additional_invite") else None,
                            ]
                        else:
                            instance["attendees"] = [
                                {'email': class_info.get("event").get("additional_invite")} if class_info.get("event").get("additional_invite") else None,
                            ]
                        updated = True

                    # If there is no one-time replacement and the teacher is not the permanent teacher, update the attendees
                    if instance_email and instance_email != permenant_email:
                        if permenant_email:
                            instance["attendees"] = [
                                {"email": permenant_email},
                                {'email': class_info.get("event").get("additional_invite")} if class_info.get("event").get("additional_invite") else None,
                            ]
                        else:
                            instance["attendees"] = [
                                {'email': class_info.get("event").get("additional_invite")} if class_info.get("event").get("additional_invite") else None,
                            ]
                        updated = True
                        if firstAllUpdate:
                            sendUpdates = "all"
                            firstAllUpdate = False
                        else:
                            sendUpdates = "none"

                # Only update the instance if it was modified
                if updated:
                    batch3.add(google.calendar.events().update(calendarId=google.CALENDAR_CLASSES_ID, eventId=instance['id'], body=instance, sendUpdates=sendUpdates), callback=callback3)

    # Callback for batch request to print final status
    def callback3(request_id, response, exception):
        if exception:
            print(f'[ERROR] In batch3: {exception}')
        else:
            print(f'[INFO] Successfully updated events for {class_info["code"]}')

    # Update the Opportunity Name if it is different from the Code
    if class_info.get("code") != class_info.get("name"):
        sf.sf.Opportunity.update(class_info["id"], {"Name": class_info["code"]})

    if not class_info.get("event", {}).get("id"):
        # Create the Google Event
        batch1.add(google.calendar.events().insert(calendarId=google.CALENDAR_CLASSES_ID, body=event, sendUpdates="all", conferenceDataVersion=1), callback=callback1)
    else:
        # Update the Google Event
        batch1.add(google.calendar.events().update(calendarId=google.CALENDAR_CLASSES_ID, eventId=class_info.get("event", {}).get("id"), body=event, sendUpdates="all", conferenceDataVersion=1), callback=callback1)

def update_and_create_classes_per_week(google, sf, year_code=None, class_code=None, class_id=None):
    # Create Batch Requests
    # batch1: Create or Update the Event
    batch1 = google.calendar.new_batch_http_request()
    # batch2: Get the Instances of the Event
    batch2 = google.calendar.new_batch_http_request()
    # batch3: Delete the Excluded Instances
    batch3 = google.calendar.new_batch_http_request()

    # Get the class details for the specified year
    if year_code:
        classes = sf.get_all_class_details(year_code)

        # Create the Events and the Pictures folder for each Camp
        for class_info in classes:
            try:
                __class_event(google, sf, class_info, batch1, batch2, batch3)
            except Exception as e:
                raise ValueError(f'[ERROR] {e}')

    elif class_code:
        # Get the class details for the specified class
        class_info = sf.get_all_class_details2(class_code)
        try:
            __class_event(google, sf, class_info, batch1, batch2, batch3)
        except Exception as e:
            raise ValueError(f'[ERROR] {e}')
    elif class_id:
        # Get the class details for the specified class
        class_info = sf.get_all_class_details3(class_id)
        print(class_info)

        try:
            __class_event(google, sf, class_info, batch1, batch2, batch3)
        except Exception as e:
            raise ValueError(f'[ERROR] {e}')

    # Execute the Batch Requests
    batch1.execute()
    batch2.execute()
    batch3.execute()

    # return "Success", True

    return "Success", True
