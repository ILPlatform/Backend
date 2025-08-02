import datetime
from functools import partial


class CampManager:
    """
    Manages the creation and updating of Google Calendar events and Drive folders for camps,
    with support for replacement and additional teacher assignments.
    """

    def __init__(self, google_service, salesforce_client):
        """
        Initializes the CampManager.

        Args:
            google_service: The authenticated Google API service object.
            salesforce_client: The authenticated Salesforce API client object.
        """
        self.google = google_service
        self.sf = salesforce_client

        # Initialize batch requests for Google Calendar API
        self.batch_event_create_update = self.google.calendar.new_batch_http_request()
        self.batch_event_get_instances = self.google.calendar.new_batch_http_request()
        self.batch_event_update_instances = self.google.calendar.new_batch_http_request()

    def _generate_event_body(self, camp_info):
        """Creates the dictionary for the Google Calendar event body with the main teacher."""
        base_attendees = []
        # Primary teacher
        if camp_info.get("teacher_email"):
            base_attendees.append({'email': camp_info["teacher_email"] if False else camp_info["teacher_email"]})
        return {
            'summary': camp_info["summary"],
            'location': camp_info["address"],
            'description': camp_info["description"],
            'start': {'dateTime': camp_info["start"], 'timeZone': 'Europe/Brussels'},
            'end': {'dateTime': camp_info["end_day1"], 'timeZone': 'Europe/Brussels'},
            'recurrence': ['RRULE:FREQ=DAILY;COUNT=5'],
            'attendees': base_attendees,
            'sendUpdates': 'all'
        }

    def _manage_picture_folders(self, camp_info):
        """Creates Google Drive folders for camp pictures if they don't exist."""
        # ... unchanged ...
        # (same as original)
        # Create holiday-specific folder if needed
        if not camp_info.get("picture_grand_parent_id"):
            folder_id = self.google.create_camp_pictures_folder(f"{camp_info.get('holiday_name')}")
            self.sf.sf.Picklist__c.update(camp_info["holiday_id"], {"Google_Drive_Pictures_ID__c": folder_id})
            camp_info["picture_grand_parent_id"] = folder_id

        # Create week-specific folder if needed
        if not camp_info.get("picture_parent_id"):
            folder_id = self.google.create_camp_pictures_folder(
                f"{camp_info.get('picture_parent_name')}", parent=camp_info["picture_grand_parent_id"]
            )
            self.sf.sf.Picklist__c.update(camp_info["week_id"], {"Google_Drive_Pictures_ID__c": folder_id})
            camp_info["picture_parent_id"] = folder_id

        # Create camp-specific folder if needed
        if not camp_info.get("pictures_id"):
            folder_id = self.google.create_camp_pictures_folder(
                f"{camp_info.get('pictures_name')}", parent=camp_info["picture_parent_id"]
            )
            self.sf.sf.Opportunity.update(camp_info["id"], {"Google_Drive_Pictures__c": folder_id})

    def _add_camp_event_to_batch(self, camp_info):
        """Handles creating or updating a single camp event via batch request."""
        # 1. Update Salesforce Opportunity Name if needed
        if camp_info.get("code") != camp_info.get("name"):
            self.sf.sf.Opportunity.update(camp_info["id"], {"Name": camp_info["code"]})

        # 2. Generate the event body
        event_body = self._generate_event_body(camp_info)

        # 3. Define the callback for the first batch request
        callback = lambda req_id, resp, exc: self._callback_event_created(req_id, resp, exc, camp_info)

        # 4. Add request to the first batch
        if not camp_info.get("event_id"):
            self.batch_event_create_update.add(
                self.google.calendar.events().insert(
                    calendarId=self.google.CALENDAR_CAMPS_ID, body=event_body, sendUpdates="all"
                ),
                callback=callback
            )
        else:
            self.batch_event_create_update.add(
                self.google.calendar.events().update(
                    calendarId=self.google.CALENDAR_CAMPS_ID, eventId=camp_info.get("event_id"), body=event_body,
                    sendUpdates="all"
                ),
                callback=callback
            )

    def _callback_event_created(self, request_id, response, exception, camp_info):
        """Callback executed after creating/updating the recurring event."""
        if exception:
            print(f'[ERROR] Batch 1 (Create/Update) for {camp_info}["code"]: {exception}')
            return

        # Update Salesforce with the Google Event ID
        event_id = response["id"]
        self.sf.update_opportunity(camp_info["id"], {"Google_Event__c": event_id})

        # Callback for retrieving instances
        callback = lambda req_id, resp, exc: self._callback_instances_retrieved(req_id, resp, exc, camp_info)

        self.batch_event_get_instances.add(
            self.google.calendar.events().instances(calendarId=self.google.CALENDAR_CAMPS_ID, eventId=event_id),
            callback=callback
        )

    def _callback_instances_retrieved(self, request_id, response, exception, camp_info):
        """Callback after retrieving instances. Handles cancellations, replacements, and additional teachers."""
        if exception:
            print(f'[ERROR] Batch 2 (Get Instances) for {camp_info}["code"]: {exception}')
            return

        # Prepare excluded days list
        excluded_days = camp_info.get("excluded_day", "").split(",") if camp_info.get("excluded_day") else []
        if camp_info.get("overwrite_cancelled"):
            for day in camp_info.get("overwrite_cancelled").split("\n"):
                excluded_days.append(datetime.datetime.strptime(day, "%d/%m/%Y").strftime("%Y-%m-%d"))
        is_excluded = lambda d: d in excluded_days

        original_teacher = camp_info.get("teacher_email")
        replacements = list(filter(lambda repl: repl["type"] == "OneTime", camp_info.get("replacements", [])))
        additional_list = list(filter(lambda repl: repl["type"] == "Additional Teacher", camp_info.get("replacements", [])))

        # Process each instance in date order
        for instance in sorted(response['items'], key=lambda item: item["start"]["dateTime"]):
            updated = False
            date_str = instance["start"]["dateTime"][:10]
            current_attendees = instance.get("attendees", [])
            current_teacher = current_attendees[0].get("email") if current_attendees else None

            # 1. Cancellation
            if is_excluded(date_str):
                if instance.get("status") != "cancelled":
                    instance["status"] = "cancelled"
                    updated = True

            else:
                # 2. Replacement
                rep = next((r for r in replacements if r["date"] == date_str), None)
                if rep:
                    new_email = rep.get("email")
                    instance["attendees"] = [{'email': new_email}] if new_email else []
                    updated = True

                elif current_teacher and current_teacher != original_teacher:
                    # If no replacement and current teacher is not the original, revert to original teacher
                    instance["attendees"] = [{'email': original_teacher}] if original_teacher else []
                    updated = True

                # 3. Additional teacher
                add = next((a for a in additional_list if a["date"] == date_str), None)
                if add:
                    add_email = add.get("email")
                    if add_email and not any(att.get("email") == add_email for att in instance.get("attendees", [])):
                        if add_email:
                            instance.setdefault("attendees", []).append({'email': add_email})
                            updated = True
                elif len(current_attendees) > 1:
                    # If there are multiple attendees and no additional teacher, revert to original teacher
                    instance["attendees"] = [{'email': original_teacher}] if original_teacher else []
                    updated = True

            if updated:
                cb = lambda req_id, resp, exc: self._callback_instance_updated(req_id, resp, exc, camp_info["code"])
                self.batch_event_update_instances.add(
                    self.google.calendar.events().update(
                        calendarId=self.google.CALENDAR_CAMPS_ID,
                        eventId=instance['id'], body=instance, sendUpdates="all"
                    ),
                    callback=cb
                )

    def _callback_instance_updated(self, request_id, response, exception, camp_code):
        """Callback after updating a single instance."""
        if exception:
            print(f'[ERROR] Batch 3 (Update Instance) for {camp_code}: {exception}')
        else:
            print(f'[INFO] Successfully updated instance for camp {camp_code}')
        # else: logging as needed

    def process_camps(self, camps):
        """Queues batch requests for multiple camps."""
        for camp_info in camps:
            try:
                self._add_camp_event_to_batch(camp_info)
                self._manage_picture_folders(camp_info)
                print(f'[INFO] Queued tasks for {camp_info.get("code")}')
            except Exception as e:
                print(f'[ERROR] Failed to queue tasks for {camp_info.get("code")}: {e}')

    def execute_batch_requests(self):
        """Executes all queued batch requests in sequence."""
        print("Executing Batch 1: Create/Update Events...")
        self.batch_event_create_update.execute()
        print("Executing Batch 2: Get Event Instances...")
        self.batch_event_get_instances.execute()
        print("Executing Batch 3: Update Instances...")
        self.batch_event_update_instances.execute()
        print("[SUCCESS] All batch operations completed.")


# ------------------------------------------------------------------------------
# Main Execution Functions (External Interface)
# ------------------------------------------------------------------------------

def update_and_create_camps_per_week(google, sf, week_codes):
    """Fetches all camps for given week codes and processes them."""
    manager = CampManager(google, sf)
    camps = sf.get_all_camp_details(week_codes)

    if camps:
        manager.process_camps(camps)
        manager.execute_batch_requests()
    else:
        print(f"No camps found for week codes: {week_codes}")

    return "Success", True


def update_and_create_camps(google, sf, camp_id):
    """Fetches a single camp by its ID and processes it."""
    # First, get the week_code from the camp_id
    result = sf.sf.query(f"SELECT Week__r.Week_Code__c FROM Opportunity WHERE Id='{camp_id}'")["records"]
    if not result:
        print(f"[ERROR] No camp found with ID: {camp_id}")
        return "Failure", False

    # Now, get all camp details for that week and filter for the specific camp
    week_code = result[0]["Week__r"]["Week_Code__c"]
    all_camps_in_week = sf.get_all_camp_details([week_code])
    target_camp = [c for c in all_camps_in_week if c["id"] == camp_id]

    if target_camp:
        manager = CampManager(google, sf)
        manager.process_camps(target_camp)
        manager.execute_batch_requests()
    else:
        print(f"Could not retrieve details for camp ID: {camp_id}")

    return "Success", True