#!/usr/bin/env python3.11

# Firebase imports
from firebase_admin import initialize_app

import os
from dotenv import load_dotenv
load_dotenv()

from Helpers import https_fn_custom

# Initialize the app
app = initialize_app()

# Import the functions
from Functions import admin_get_week_codes, admin_create_camps_form, admin_update_camps_events, admin_get_teachers_partners, admin_create_teacher_convention, admin_create_teacher_attestations, admin_update_teacher_contract_signed

@https_fn_custom()
def admin_test(request):
    return {"data": {"response": request.remote_addr, "status": 200}}
