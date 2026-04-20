import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from Logger import log

# Constants
TOKEN_PATH = os.path.join(os.getcwd(), '.googleapi_token.json')
CREDENTIALS_PATH = os.path.join(os.getcwd(), '.googleapi_credentials.json')
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/contacts'
]
CAMPS_FORM_ID = os.getenv("CAMPS_FORM_ID")
CALENDAR_CAMPS_ID = os.getenv("CALENDAR_CAMPS_ID")
# DRIVE_CAMPS_PHOTOS_ID = os.getenv("DRIVE_CAMPS_PHOTOS_ID")
CAMPS_FORM_DRIVE_ID = os.getenv("CAMPS_FORM_DRIVE_ID")


class GoogleConnector():
    CALENDAR_CAMPS_ID = os.getenv("CALENDAR_CAMPS_ID")
    CALENDAR_CLASSES_ID = os.getenv("CALENDAR_CLASSES_ID")
    CLASSES_FORM_ID = os.getenv("CLASSES_FORM_ID")

    def __init__(self, token=None):
        if token:
            self.auth = self.__authorize_with_token(token)
        else:
            self.auth = self.__authorize_without_token()
        self.__build_services()
        log("AUTHENTICATE", "Google", "Connected to Google APIs")

    def __build_services(self):
        self.__build_calendar()
        self.__build_drive()
        self.__build_forms()
        self.__build_docs()
        self.__build_sheets()
        self.__build_contacts()

    def __build_calendar(self):
        try:
            self.calendar = build('calendar', 'v3', credentials=self.auth)
        except Exception as e:
            self.calendar = None
            log("ERROR", "Google", f"Calendar not built. Error: {e}")

    def __build_drive(self):
        try:
            self.drive = build('drive', 'v3', credentials=self.auth)
        except Exception as e:
            self.drive = None
            log("ERROR", "Google", f"Drive not built. Error: {e}")

    def __build_forms(self):
        try:
            self.forms = build('forms', 'v1', credentials=self.auth)
        except Exception as e:
            self.forms = None
            log("ERROR", "Google", f"Forms not built. Error: {e}")

    def __build_docs(self):
        try:
            self.docs = build('docs', 'v1', credentials=self.auth)
        except Exception as e:
            self.docs = None
            log("ERROR", "Google", f"Docs not built. Error: {e}")

    def __build_sheets(self):
        try:
            self.sheets = build('sheets', 'v4', credentials=self.auth)
        except Exception as e:
            self.sheets = None
            log("ERROR", "Google", f"Sheets not built. Error: {e}")

    def __build_contacts(self):
        try:
            self.contacts = build('people', 'v1', credentials=self.auth)
        except Exception as e:
            self.contacts = None
            log("ERROR", "Google", f"Contacts not built. Error: {e}")

    # Authorize and return a Google API client using a provided token
    def __authorize_with_token(self, token):
        try:
            log("AUTHENTICATE", "Google", "Authenticating with pre-existing Google credentials")
            return Credentials(
                token=token,
                scopes=SCOPES
            )
        except Exception as e:
            log("ERROR", "Google", f"Authentication failed: {e}")
            exit()

    # Authorize and return a Google API client without a provided token
    def __authorize_without_token(self):
        try:
            log("AUTHENTICATE", "Google", "Creating Google credentials")
            # Load saved credentials if they exist
            credentials = None
            if os.path.exists(TOKEN_PATH):
                with open(TOKEN_PATH, 'r') as token_file:
                    credentials = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

            if not credentials or not credentials.valid:
                log("AUTHENTICATE", "Google", "Token non-existing, generating file")
                if credentials and credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                    credentials = flow.run_local_server(
                        host="localhost",
                        port=8888,
                        access_type='offline',
                        prompt='consent'
                    )

                # Save credentials to a file
                with open(TOKEN_PATH, 'w') as token_file:
                    token_file.write(credentials.to_json())

            return credentials
        except Exception as e:
            log("ERROR", "Google", f"Authentication failed: {e}")
            exit()

    def create_event(self, event):
        return self.calendar.events().insert(calendarId=CALENDAR_CAMPS_ID, body=event).execute()

    def update_event(self, event_id, event):
        return self.calendar.events().update(calendarId=CALENDAR_CAMPS_ID, eventId=event_id, body=event).execute()

    def create_camps_form(self):
        # Create body for form allowing daniel@ilplatform.be to edit
        body = {
            "addParents": [CAMPS_FORM_DRIVE_ID]
        }

        return self.drive.files().copy(fileId=CAMPS_FORM_ID, body=body).execute()

    def update_form(self, form_id, update):
        # Update Form
        result = self.forms.forms().batchUpdate(formId=form_id, body=update).execute()

        # Get Form
        form = self.forms.forms().get(formId=form_id).execute()

        return form

    def publish_form(self, form_id):
        body = {
            "publishSettings": {
                "publishState": {
                    "isPublished": True,
                    "isAcceptingResponses": True,
                }
            },
            "updateMask": "publish_state",
        }

        return self.forms.forms().setPublishSettings(formId=form_id, body=body).execute()

    # def create_camp_pictures_folder(self, name, parent=None):
    #     # Create the folder
    #     file_metadata = {
    #         'name': name,
    #         'mimeType': 'application/vnd.google-apps.folder'
    #     }
    #     file = self.drive.files().create(body=file_metadata, fields='id, parents').execute()
    #
    #     # Move the folder
    #     previous_parents = ",".join(file.get("parents"))
    #     file = self.drive.files().update(
    #                 fileId=file.get("id"),
    #                 addParents=parent or DRIVE_CAMPS_PHOTOS_ID,
    #                 removeParents=previous_parents,
    #                 fields="id",
    #             ).execute()
    #     return file.get("id")

    # def update_camp_pictures_folder(self, id, name, parent=None):
    #     file = self.drive.files().get(fileId=id, fields='id, parents').execute()
    #     file_metadata = {
    #         'name': name,
    #     }
    #     previous_parents = ",".join(file.get("parents"))
    #     file = self.drive.files().update(
    #                 body=file_metadata,
    #                 fileId=id,
    #                 addParents=parent or DRIVE_CAMPS_PHOTOS_ID,
    #                 removeParents=previous_parents,
    #                 fields="id",
    #             ).execute()
    #     return file.get("id")
