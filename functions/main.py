#!/usr/bin/env python3.11

# Firebase imports
from firebase_admin import initialize_app, credentials

import os
from dotenv import load_dotenv
load_dotenv()

from Helpers import https_fn_custom

# Initialize the app
# Path to your service account key JSON file
SERVICE_ACCOUNT_PATH = ".firebase_adminsdk.json"
if not os.path.exists(SERVICE_ACCOUNT_PATH):
    raise ValueError("Firebase service account file not found!")

# Initialize Firebase Admin SDK with explicit credentials
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
app = initialize_app(cred)

# Import the functions
from Functions import admin_get_week_codes, admin_create_camps_form, admin_update_camps_events, admin_get_teachers_partners, admin_create_teacher_convention, admin_update_teacher_contract_signed, admin_update_classes_events, admin_update_single_class_events #, admin_create_teacher_attestations

from Replacements import *
from Curriculum import *
from Landing import *
