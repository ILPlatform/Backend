# Functions

## Running Emulator

The first time you run the emulator, you will need to run the following;

```
cd functions
source venv/bin/activate
pip3 install -r requirements.txt
```

In order to run the emulator, you need to run the following;

```
firebase emulators:start --only functions
```

## Deployment

In order to deploy the functions, you need to run the following;

```
firebase deploy --only functions
```

## Installing Modules

In order to install a module in the backend, add it to `functions/requirements/txt` and run the following;

```
cd functions
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Available Functions

**List to be made**

## Environment File

The `.env` file is used to store the environment variables. The `.env` file is not included in the repository for security reasons. The `.env` file should be created in the `functions` folder and should contain the following environment variables:

```
# Salesforce Login Details. Note SF_DOMAIN can be left blank if you are using the standard Salesforce domain.
SF_USERNAME=
SF_PASSWORD=
SF_SECURITY_TOKEN=
SF_DOMAIN=

# Gmail Login Details (See https://support.google.com/mail/answer/185833?hl=en for details)
GMAIL_USER_EMAIL=
GMAIL_PASSWORD=

# Google Calendar IDs
CALENDAR_CLASSES_ID=
CALENDAR_CAMPS_ID=

# Document Template IDs
ATTESTATION_TEMPLATE_ID=1DiT2wj3ZpaZzzX1ACT1igQdqhyfebl_7lbKQw1Ubego
PRESTATION_TEMPLATE_ID=1guzoO5hwGgqpphVp-i9dGAAiM8wojnzpe4Qlk9-yZY4
CONVENTION_TEMPLATE_ID=108r2FThPRfhT_MlrZApP1I8V-Oqf7gADnfg5BCSFUcY
PAYMENTS_TEMPLATE_ID=1GvMd45uiYVMKo_UzJSwM02Z_kle06OO88Ep8bqgNSL4
STUDENT_CONTRACT_TEMPLATE_ID=1ix8fbFDB-GX44cy9s0M6cVpIWgvQ2DpOYX0JDCPucys
VOLUNTEER_CONTRACT_TEMPLATE_ID=1VlC0s109q15lpJbMA5vTFJojYtNSRVz7uTrnWIUimQs

# Google Drive Folder IDs
DOCUMENTS_BY_BOT_ID=
DRIVE_CAMPS_PHOTOS_ID=

# Google Sheets Payment Document
SHEETS_PAYMENTS_ID=

# Salesforce Standard IDs
SF_TEACHERS_ACCOUNT_ID=0010600002Fm3UIAAZ
SF_TEACHER_CONTRACT_RECORD_TYPE_ID=012P5000001H6wTIAS
```

In testing mode, you may use the different testing files available. Here are the additional keys to add to the `.env` file:

```
# Both equal, are the Testing Calendar. Note items will appear twice since the same calendar is used for both.
CALENDAR_CLASSES_ID=c_cdc8989cda044e59658cf83909eff1146e343eb44ec96c3a395eb292e4ca6295@group.calendar.google.com
CALENDAR_CAMPS_ID=c_cdc8989cda044e59658cf83909eff1146e343eb44ec96c3a395eb292e4ca6295@group.calendar.google.com

# Folder IDs, in the folder "Testing" which you need access to
DOCUMENTS_BY_BOT_ID=1NtvJFfR6S86XlZGDgEolPurSbb6Ws4mi
DRIVE_CAMPS_PHOTOS_ID=10mw45EehzV4sSWSHUCe-m_kfV8mO30bh

# Google Sheets Payment Document, again in the "Testing" folder
SHEETS_PAYMENTS_ID=1dAaVcugCCvYESW1oAdb-TaCS5-zmHT6WoqFD7zpgjwc
```

In either case, you will need to provide the Salesforce login details and Gmail login details with your own credentials.
