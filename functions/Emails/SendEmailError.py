import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from .Contents import html_error
from .SendEmailSetup import create_smtp_transport, GMAIL_REPLY_TO, GMAIL_PASSWORD, GMAIL_ADMIN_TO, GMAIL_SENDER

# Send attestation mail (to teacher and admin)
def send_email_error(error):
    # Setup email parameters
    subject = "[ERROR] Error occured on Admin Backend ILPlatform"

    # Creating the email message
    msg = MIMEMultipart()
    msg['From'] = GMAIL_SENDER
    msg['Reply-to'] = GMAIL_REPLY_TO
    msg['To'] = GMAIL_REPLY_TO
    msg['Subject'] = subject
    msg.attach(MIMEText(html_error(error), 'html'))

    # Send the email
    server = create_smtp_transport()
    try:
        server.sendmail(GMAIL_SENDER, GMAIL_REPLY_TO, msg.as_string())
        print(f"[SUCCESS] Error Email Sent Successfully")
    except Exception as e:
        raise ConnectionError(f"[ERROR] Error in sending email: {e}")
    finally:
        server.quit()
