import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from .SendEmailSetup import create_smtp_transport, GMAIL_REPLY_TO, GMAIL_PASSWORD, GMAIL_ADMIN_TO, GMAIL_SENDER
from .Contents.htmlSignature import html_signature

# Send replacement confirmation email
def send_email_replacement_onetime(email, class_name, date):
    # Setup template parameters
    params = {
        'class_name': class_name,
        'date': date
    }

    # Setup email parameters
    subject = "Confirmation de réception de demande de remplacement"

    # Creating the email message
    msg = MIMEMultipart()
    msg['From'] = GMAIL_SENDER
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_replacement(params), 'html'))

    # Send the email
    server = create_smtp_transport()
    try:
        server.sendmail(GMAIL_SENDER, email + ", " + GMAIL_REPLY_TO, msg.as_string())
        print(f"[SUCCESS] Email Sent Successfully")
    except Exception as e:
        print(f"[ERROR] Error in sending email: {e}")
    finally:
        server.quit()

# Send replacement confirmation email to admin
def send_email_replacement_onetime_admin(email, class_name, date):
    # Setup template parameters
    params = {
        'email': email,
        'class_name': class_name,
        'date': date
    }

    # Setup email parameters
    subject = "Nouveau remplacement"

    # Creating the email message
    msg = MIMEMultipart()
    msg['From'] = GMAIL_SENDER
    msg['To'] = GMAIL_ADMIN_TO
    msg['Subject'] = subject
    msg.attach(MIMEText(html_replacement_admin(params), 'html'))

    # Send the email
    server = create_smtp_transport()
    try:
        server.sendmail(GMAIL_SENDER, GMAIL_ADMIN_TO, msg.as_string())
        print(f"[SUCCESS] Email Sent Successfully")
    except Exception as e:
        print(f"[ERROR] Error in sending email: {e}")
    finally:
        server.quit()

# Generate HTML for replacement confirmation email
def html_replacement(params):
    return f"""
    <p>
        Bonjour,
    </p>
    <p>
        Ta demande de remplacement a bien été reçue pour :
    </p>
    <ul>
        <li><b>Cours :</b> {params.get('class_name')}</li>
        <li><b>Date :</b> {params.get('date')}</li>
    </ul>
    <p>
        Si cette demande est de dernière minute (moins de 24h), merci de nous contacter également via WhatsApp au plus vite.
    </p>
    <p>
        Merci de ne pas répondre à cet email. Si tu as des questions, merci de nous contacter via WhatsApp ou via <a href="mailto:daniel@ilplatform.be">daniel@ilplatform.be</a>.
    </p>
    <p>
        Merci et bien à toi,
    </p>
    {html_signature()}
    """

# Generate HTML for replacement confirmation email to admin
def html_replacement_admin(params):
    return f"""
    <p>
        Bonjour,
    </p>
    <p>
        Une demande de remplacement a été reçue pour :
    </p>
    <ul>
        <li><b>Email :</b> {params.get('email')}</li>
        <li><b>Cours :</b> {params.get('class_name')}</li>
        <li><b>Date :</b> {params.get('date')}</li>
    </ul>
    <p>
        Bien à toi,
    </p>
    {html_signature()}
    """
