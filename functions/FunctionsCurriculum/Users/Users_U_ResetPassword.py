from Helpers import firebase_functions_custom, https_fn_custom
from firebase_admin import auth
from Salesforce import getSF
from Emails import sendEmail


@https_fn_custom()
@firebase_functions_custom(auth_level=0)
def users_u_reset_password(data):
    # Initialize SF
    sf = getSF()

    # Get the parameters
    email = data.get("email")

    # Give user claims
    if not email:
        return {"data": {"response": "email is required", "status": 400}}

    # Generate password reset link
    action_code_settings = auth.ActionCodeSettings(
        url="https://curriculum.ilplatform.be",
        handle_code_in_app=True,
    )
    reset_link = auth.generate_password_reset_link(email, action_code_settings)

    # Get the user name
    details = sf.sf.query(f"SELECT Name FROM Employee__c WHERE Email__c='{email}'").get("records")[0]

    # Send email to the user
    sendEmail("reset_password_user", {"Name": details["Name"], "ResetLink": reset_link}, email)

    return {
        "data": {
            "response": "Success",
            "status": 200
        }
    }
