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
from Functions import admin_get_week_codes, admin_create_camps_form, admin_update_camps_events, admin_get_teachers_partners, admin_create_teacher_convention, admin_update_teacher_contract_signed, admin_update_classes_events, admin_update_single_class_events #, admin_create_teacher_attestations

from Replacements import replacements_create_one_time, replacements_create_permanent, replacements_get_one_time, replacements_delete, replacements_get_all_user, replacements_solve, replacements_create, replacements_create_user

from Curriculum import *
