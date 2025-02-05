import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Environment, FileSystemLoader
from .SendEmailSetup import create_smtp_transport, GMAIL_REPLY_TO, GMAIL_PASSWORD, GMAIL_ADMIN_TO, GMAIL_SENDER
from .Contents.htmlSignature import html_signature
import requests

# Send replacement confirmation email
def send_email_new_document(email, description, link=None):
    # Setup template parameters
    params = {
        'description': description
    }

    # Setup email parameters
    subject = "Nouveau Document Disponible"

    # Creating the email message
    msg = MIMEMultipart()
    msg['From'] = GMAIL_SENDER
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_new_document(params), 'html'))

    # Download the attachment if it exists
    if link:
        local_file_path = "/tmp/sample.pdf"
        response = requests.get(link)
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
        server.sendmail(GMAIL_SENDER, email + ", " + GMAIL_REPLY_TO, msg.as_string())
        print(f"[SUCCESS] Email Sent Successfully")
    except Exception as e:
        print(f"[ERROR] Error in sending email: {e}")
    finally:
        server.quit()

# Generate HTML for replacement confirmation email
def html_new_document(params):
    return f"""
    <p>
        Bonjour,
    </p>
    <p>
        Un nouveau document ({params.get('description')}) est disponible pour toi. Tu peux le retrouver sur le <a href="https://curriculum.ilplatform.be">site curriculum</a>, sous "My Account" > "Documents".
    </p>
    <p>
        Merci de ne pas répondre à cet email. Si tu as des questions, merci de nous contacter via WhatsApp ou via <a href="mailto:daniel@ilplatform.be">daniel@ilplatform.be</a>.
    </p>
    <p>
        Merci et bien à toi,
    </p>
    {html_signature()}
    """
