# Firebase imports
from firebase_admin import initialize_app

# Initialize the app
app = initialize_app()

# Import the functions
from Functions import  admin_get_week_codes, admin_create_camps_form, admin_update_camps_events, admin_get_teachers_partners
