from Emails import send_email_user

def sendEmail_resetPasswordUser(email, details):
    send_email_user(
        email,
        subject="Reset your Password for ILPlatform",
        body=f"""
        <p>Hello {details.get("Name")},</p>
        <p>Your password has been successfully reset. To continue, please follow the steps below:</p>
        <ol>
            <li><strong>Change your password:</strong> Click on the following link to set a new password: <a href="{details.get("ResetLink")}">Change my password</a>.</li>
            <li><strong>Log in to the platform:</strong> After changing your password, you can log in to the ILPlatform curriculum website using the <a href="https://curriculum.ilplatform.be">following link</a>.</li>
        </ol>
        <p>Remember, the curriculum website is your central hub for all information related to your classes, personal documents, and administrative procedures. We encourage you to log in as soon as possible to ensure you have access to all the resources you need.</p>
        <p>Thank you and best regards,</p>
        """
    )