import os
import smtplib

# Environment variables
GMAIL_USER_EMAIL = os.getenv("GMAIL_USER_EMAIL")
GMAIL_SENDER = f"HR ILPlatform <{GMAIL_USER_EMAIL}>"
GMAIL_REPLY_TO = GMAIL_USER_EMAIL
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
if os.getenv("FUNCTIONS_EMULATOR") == "true":
    GMAIL_ADMIN_TO = "daniel@ilplatform.be"
else:
    GMAIL_ADMIN_TO = "daniel@ilplatform.be,eimantas@ilplatform.be"

# SMTP setup
def create_smtp_transport():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(GMAIL_USER_EMAIL, GMAIL_PASSWORD)
    return server
