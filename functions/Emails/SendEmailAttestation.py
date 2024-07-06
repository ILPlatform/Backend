import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from .Contents.htmlAttestation import html_attestation_teacher, html_attestation_admin
from .SendEmailSetup import create_smtp_transport, GMAIL_REPLY_TO, GMAIL_PASSWORD, GMAIL_ADMIN_TO, GMAIL_SENDER

# Send attestation mail (to teacher)
def send_attestation_teacher(teacher, year, month, single):
    month_names = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    month_shift = month - 1
    month = month_names[month_shift]
    nextMonth = month_names[0] if month_shift == 11 else month_names[month_shift + 1]
    nextYear = year + 1 if month_shift == 11 else year

    # Setup template parameters
    params = {
        'name': teacher.get('name').split(' ')[0],
        'month': month,
        'nextMonth': nextMonth,
        'year': year,
        'nextYear': nextYear,
        'sharableLink': teacher.get('link')
    }

    # Setup email parameters
    subject = f"{'CORRECTION' if single else ''} Prestations {month} {year}" if teacher.get('contract') else f"Attestation {month} {year}"

    # Creating the email message
    msg = MIMEMultipart()
    msg['From'] = GMAIL_SENDER
    msg['Reply-to'] = GMAIL_REPLY_TO
    msg['To'] = teacher.get('email')
    msg['Subject'] = subject
    msg.attach(MIMEText(html_attestation_teacher(params), 'html'))

    # Send the email
    server = create_smtp_transport()
    try:
        server.sendmail(GMAIL_SENDER, teacher.get('email'), msg.as_string())
        print(f"[SUCCESS] {teacher.get('name')} - Email Sent Successfully")
    except Exception as e:
        raise SystemError(f"[ERROR] {teacher.get('name')} - Error in sending email: {e}")
    finally:
        server.quit()

# Send attestation mail (to admin)
def send_attestation_admin(admin_mail, year, month):
    month_names = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    month_shift = month - 1
    month = month_names[month_shift]

    # Setup template parameters
    params = {
        'month': month,
        'year': year,
        'admin_mail': "\n".join(admin_mail)
    }

    # Setup email parameters
    subject = f"Admin Attestations {month} {year}"

    # Creating the email message
    msg = MIMEMultipart()
    msg['From'] = GMAIL_SENDER
    msg['Reply-to'] = GMAIL_REPLY_TO
    msg['To'] = GMAIL_ADMIN_TO
    msg['Subject'] = subject
    msg.attach(MIMEText(html_attestation_admin(params), 'html'))

    # Send the email
    server = create_smtp_transport()
    try:
        server.sendmail(GMAIL_SENDER, GMAIL_ADMIN_TO, msg.as_string())
        print(f"[SUCCESS] ADMIN - Email Sent Successfully")
    except Exception as e:
        raise SystemError(f"[ERROR] ADMIN - Error in sending email: {e}")
    finally:
        server.quit()
