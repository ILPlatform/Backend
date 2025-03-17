# ILPlatform Backend

## Setup

In order for the code to make sense, you need to generate the following files:

- `functions/.googleapi_credentials.json` - Can be obtained through the Google Cloud Console under Credentials > OAuth
  2.0 Client IDs with type Web Application and redirect URI "http://localhost:8888/oauth2callback".
- `functions/.googleapi_token.json` - Can be obtained by running the server locally (see below) and calling any endpoint
  that requires the Google Connector. Ensure that all scopes are activated in the Google API.
- `functions/.firebase_adminsdk.json` - Can be obtained through the Firebase Console under Project Settings > Service
  Accounts > Generate New Private Key.
- `functions/.env` - Contains the following environment
  variables:
  ```env
  # Salesforce Login Details (to access database)
  SF_USERNAME=
  SF_PASSWORD=
  SF_SECURITY_TOKEN=
  
  # Gmail Login Details (to send emails)
  GMAIL_USER_EMAIL=
  GMAIL_PASSWORD=
  
  # Google Calendar IDs
  CALENDAR_CLASSES_ID=
  CALENDAR_CAMPS_ID=
  CALENDAR_TESTING_ID=
  
  # Document Template IDs
  ATTESTATION_TEMPLATE_ID=
  PRESTATION_TEMPLATE_ID=
  CONVENTION_TEMPLATE_ID=
  PAYMENTS_TEMPLATE_ID=
  STUDENT_CONTRACT_TEMPLATE_ID=
  VOLUNTEER_CONTRACT_TEMPLATE_ID=
  
  # Google Form Template IDs
  CLASSES_FORM_ID=
  CAMPS_FORM_ID=
  
  # Google Drive Folder IDs
  DOCUMENTS_BY_BOT_ID=
  DRIVE_CAMPS_PHOTOS_ID=
  
  # Google Sheet IDs
  SHEETS_PAYMENTS_ID=
  
  # Salesforce Standard IDs
  SF_TEACHERS_ACCOUNT_ID=
  SF_TEACHER_CONTRACT_RECORD_TYPE_ID=
  
  # WhatsApp Configuration
  WHATSAPP_ACCESS_TOKEN=
  WHATSAPP_PHONE_ID=
  WHATSAPP_ADMINS_TEST=
  WHATSAPP_ADMINS=
  ```
- `functions/venv` - Contains the Python virtual environment for the backend. Can be created by running
  ```bash
  cd functions
  python3.11 -m venv venv
  source venv/bin/activate
  python3.11 -m pip install -r requirements.txt 
  ```
## Local Development

In order to run the code, you need to run the following;

```
. functions/venv/bin/activate
firebase emulators:start --only functions
```