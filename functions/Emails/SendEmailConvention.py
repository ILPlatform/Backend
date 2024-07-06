import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from .Contents.htmlConvention import html_convention
from .SendEmailSetup import create_smtp_transport, GMAIL_REPLY_TO, GMAIL_PASSWORD, GMAIL_ADMIN_TO, GMAIL_SENDER

# Send attestation mail (to teacher and admin)
def send_convention(teacher):
    # Setup template parameters
    params = {
        'name': teacher.get('name').split(' ')[0],
        'sharableLink': teacher.get('link')
    }

    # Setup email parameters
    subject = "Convention ILPlatform"

    # Creating the email message
    msg = MIMEMultipart()
    msg['From'] = GMAIL_SENDER
    msg['Reply-to'] = GMAIL_REPLY_TO
    msg['To'] = teacher.get('email')
    msg['Subject'] = subject
    msg.attach(MIMEText(html_convention(params), 'html'))

    # Send the email
    server = create_smtp_transport()
    try:
        server.sendmail(GMAIL_SENDER, teacher.get('email') + ", " + GMAIL_REPLY_TO, msg.as_string())
        print(f"[SUCCESS] {teacher.get('name')} - Email Sent Successfully")
    except Exception as e:
        print(f"[ERROR] {teacher.get('name')} - Error in sending email: {e}")
    finally:
        server.quit()
