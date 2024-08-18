import json
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

# Constants
TOKEN_PATH = os.path.join(os.getcwd(), '.googleapi_token.json')
CREDENTIALS_PATH = os.path.join(os.getcwd(), '.googleapi_credentials.json')
SCOPES = [
  'https://www.googleapis.com/auth/calendar',
  'https://www.googleapis.com/auth/drive',
  'https://www.googleapis.com/auth/forms.body',
  'https://www.googleapis.com/auth/documents',
  'https://www.googleapis.com/auth/spreadsheets'
]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
CAMPS_FORM_ID = "1pFYz_J2dwGJ6SGoixtmnILJRfssPJevXaXUWIO73-Dw"
CALENDAR_CAMPS_ID = os.getenv("CALENDAR_CAMPS_ID")
DRIVE_CAMPS_PHOTOS_ID = os.getenv("DRIVE_CAMPS_PHOTOS_ID")

class GoogleConnector():
    CALENDAR_CAMPS_ID = os.getenv("CALENDAR_CAMPS_ID")
    CALENDAR_CLASSES_ID = os.getenv("CALENDAR_CLASSES_ID")


    def __init__(self):
        self.auth = self.__authorize()
        self.__build_services()

    def __build_services(self):
        self.__build_calendar()
        self.__build_drive()
        self.__build_forms()
        self.__build_docs()
        self.__build_sheets()

    def __build_calendar(self):
        try:
            self.calendar = build('calendar', 'v3', credentials=self.auth)
            print("[AUTHENTICATE] Calendar authenticated successfully")
        except Exception as e:
            self.calendar = None
            print(f"[ERROR] Calendar not built. Error: {e}")

    def __build_drive(self):
        try:
            self.drive = build('drive', 'v3', credentials=self.auth)
            print("[AUTHENTICATE] Drive authenticated successfully")
        except Exception as e:
            self.drive = None
            print(f"[ERROR] Drive not built. Error: {e}")

    def __build_forms(self):
        try:
            self.forms = build('forms', 'v1', credentials=self.auth)
            print("[AUTHENTICATE] Forms authenticated successfully")
        except Exception as e:
            self.forms = None
            print(f"[ERROR] Forms not built. Error: {e}")

    def __build_docs(self):
        try:
            self.docs = build('docs', 'v1', credentials=self.auth)
            print("[AUTHENTICATE] Docs authenticated successfully")
        except Exception as e:
            self.docs = None
            print(f"[ERROR] Docs not built. Error: {e}")

    def __build_sheets(self):
        try:
            self.sheets = build('sheets', 'v4', credentials=self.auth)
            print("[AUTHENTICATE] Sheets authenticated successfully")
        except Exception as e:
            self.sheets = None
            print(f"[ERROR] Sheets not built. Error: {e}")


    # Authorize and return a Google API client
    def __authorize(self):
        try:
            # Load saved credentials if they exist
            credentials = None
            if os.path.exists(TOKEN_PATH):
                print("[AUTHENTICATE] Token exists, loading file")
                with open(TOKEN_PATH, 'r') as token_file:
                    credentials = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

            if not credentials or not credentials.valid:
                print("[AUTHENTICATE] Token non-existing, generating file")
                if credentials and credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                else:
                    with open(CREDENTIALS_PATH, 'r') as creds_file:
                        info = json.load(creds_file)
                    flow = InstalledAppFlow.from_client_config(info, SCOPES)
                    credentials = flow.run_local_server(host="localhost", port=8888)

                # Save credentials to a file
                with open(TOKEN_PATH, 'w') as token_file:
                    token_file.write(credentials.to_json())

            print("[AUTHENTICATE] Authentication successful")

            return credentials
        except Exception as e:
            print(f"[ERROR] Authentication failed: {e}")
            exit()

    def create_event(self, event):
        print("CAMPS ID: ", CALENDAR_CAMPS_ID)
        return self.calendar.events().insert(calendarId=CALENDAR_CAMPS_ID, body=event).execute()

    def update_event(self, event_id, event):
        return self.calendar.events().update(calendarId=CALENDAR_CAMPS_ID, eventId=event_id, body=event).execute()

    def create_camps_form(self):
        # Create body for form allowing daniel@ilplatform.be to edit
        body = {
            "addParents": ["1llQJfvK-FNlQ26-9HmUXWKALy59cr8uM"]
        }

        return self.drive.files().copy(fileId=CAMPS_FORM_ID, body=body).execute()

    def update_form(self, form_id, update):
        # Update Form
        result = self.forms.forms().batchUpdate(formId=form_id, body=update).execute()

        # Get Form
        form = self.forms.forms().get(formId=form_id).execute()

        return form

    def create_camp_pictures_folder(self, name, parent=None):
        # Create the folder
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.drive.files().create(body=file_metadata, fields='id, parents').execute()

        # Move the folder
        previous_parents = ",".join(file.get("parents"))
        file = self.drive.files().update(
                    fileId=file.get("id"),
                    addParents=parent or DRIVE_CAMPS_PHOTOS_ID,
                    removeParents=previous_parents,
                    fields="id",
                ).execute()
        return file.get("id")

    def update_camp_pictures_folder(self, id, name, parent=None):
        file = self.drive.files().get(fileId=id, fields='id, parents').execute()
        file_metadata = {
            'name': name,
        }
        previous_parents = ",".join(file.get("parents"))
        file = self.drive.files().update(
                    body=file_metadata,
                    fileId=id,
                    addParents=parent or DRIVE_CAMPS_PHOTOS_ID,
                    removeParents=previous_parents,
                    fields="id",
                ).execute()
        return file.get("id")
