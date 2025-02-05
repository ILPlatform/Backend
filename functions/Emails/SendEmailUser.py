import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests

from .Contents import html_signature
from .SendEmailSetup import create_smtp_transport, GMAIL_REPLY_TO, GMAIL_SENDER

def send_email_user(email, subject, body, file_url=None, file_name=None):
    # Creating the email message
    msg = MIMEMultipart()
    msg['From'] = GMAIL_SENDER
    msg['Reply-to'] = GMAIL_REPLY_TO
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body + html_signature(), 'html'))

    # Download the attachment if it exists
    if file_url:
        if file_name:
            file_name = file_name.replace(' ', '_').replace('/', '_').replace('.', '_')
            local_file_path = f"/tmp/{file_name}.pdf"
        else:
            local_file_path = "/tmp/file.pdf"
        response = requests.get(file_url)
        if response.status_code == 200:
            with open(local_file_path, "wb") as file:
                file.write(response.content)
        else:
            return "Failed to download the file"

        # Attach the PDF file
        with open(local_file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(local_file_path)}")
        msg.attach(part)

    # Send the email
    server = create_smtp_transport()
    try:
        server.sendmail(GMAIL_SENDER, email, msg.as_string())
        print("[SUCCESS] USER - Email Sent Successfully")
    except Exception as e:
        raise SystemError(f"[ERROR] USER - Error in sending email: {e}")
    finally:
        server.quit()
