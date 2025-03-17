from .ReplacementsAdmin import sendEmail_ReplacementsAdmin
from .ReimbursementsAdmin import sendEmail_ReimbursementsAdmin

def sendEmail(type, details):
    if type == "replacement_admin":
        sendEmail_ReplacementsAdmin(details)
    elif type == "reimbursements_admin":
        sendEmail_ReimbursementsAdmin(details)
    else:
        raise ValueError("Invalid email type")
