# ILPlatform Backend

This repo constitutes the backend for the ILPlatform landing and curriculum page. It is built using Firebase Functions
and connects to the Salesforce and Google API for database and document management.

## Setup

In order for the code to make sense, you need to generate the following files:

- `functions/.googleapi_credentials.json` - Can be obtained through the Google Cloud Console under Credentials > OAuth
  2.0 Client IDs with type Web Application and redirect URI "http://localhost:8888/oauth2callback".
- `functions/.googleapi_token.json` - Can be obtained by running the server locally (see below) and calling any endpoint
  that requires the Google Connector. Ensure that all required scopes are activated in the Google API.
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
  
  # WhatsApp Configuration
  WHATSAPP_ACCESS_TOKEN=
  WHATSAPP_PHONE_ID=
  
  # Google Drive Folder ID (public folder to store photos)
  DRIVE_CAMPS_PHOTOS_ID
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