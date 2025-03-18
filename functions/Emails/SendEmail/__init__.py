from .ReplacementsAdmin import sendEmail_ReplacementsAdmin
from .ReimbursementsAdmin import sendEmail_ReimbursementsAdmin
from .ResetPasswordUser import sendEmail_resetPasswordUser

def sendEmail(type, details, email=None):
    if type == "replacement_admin":
        sendEmail_ReplacementsAdmin(details)
    elif type == "reimbursements_admin":
        sendEmail_ReimbursementsAdmin(details)
    elif type == "reset_password_user":
        if not email:
            print("[ERROR] Email is required for reset_password_user")
            raise ValueError("Email is required for reset_password_user")
        sendEmail_resetPasswordUser(email, details)
    else:
        print("[ERROR] Invalid email type")
        raise ValueError("Invalid email type")
