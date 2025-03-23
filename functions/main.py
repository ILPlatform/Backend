#!/usr/bin/env python3.11

# Firebase imports
from firebase_admin import initialize_app, credentials

import os
from dotenv import load_dotenv
load_dotenv()
load_dotenv('config.env')

# Initialize the app
SERVICE_ACCOUNT_PATH = ".firebase_adminsdk.json"
if not os.path.exists(SERVICE_ACCOUNT_PATH):
    raise ValueError("Firebase service account file not found!")

# Initialize Firebase Admin SDK with explicit credentials
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
app = initialize_app(cred)

# Import all functions
from FunctionsCurriculum import *
from FunctionsLanding import *