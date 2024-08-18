import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

from .Contents import html_signature
from .SendEmailSetup import create_smtp_transport, GMAIL_REPLY_TO, GMAIL_PASSWORD, GMAIL_ADMIN_TO, GMAIL_SENDER

def send_email_user(email, subject, body):
    # Creating the email message
    msg = MIMEMultipart()
    msg['From'] = GMAIL_SENDER
    msg['Reply-to'] = GMAIL_REPLY_TO
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body + html_signature(), 'html'))

    # Send the email
    server = create_smtp_transport()
    try:
        server.sendmail(GMAIL_SENDER, email, msg.as_string())
        print(f"[SUCCESS] USER - Email Sent Successfully")
    except Exception as e:
        raise SystemError(f"[ERROR] USER - Error in sending email: {e}")
    finally:
        server.quit()
