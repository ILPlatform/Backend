import datetime as dt
import html
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from zoneinfo import ZoneInfo

from firebase_functions import options, scheduler_fn

from Emails.Contents import html_signature
from Emails.SendEmailSetup import GMAIL_REPLY_TO, GMAIL_SENDER, create_smtp_transport
from FunctionsCurriculum.Events.getSchedule import getSchedule
from Salesforce import getSF


LOCAL_TIMEZONE = ZoneInfo("Europe/Brussels")
DAILY_CLASSES_EMAIL_TO = os.getenv("DAILY_CLASSES_EMAIL_TO")
PERMANENT_REPLACEMENT_TYPE_ID = "012P5000001QAUbIAO"
ONE_TIME_REPLACEMENT_TYPE_ID = "012P5000001QASzIAO"


def _format_time(value):
    return value[:5] if value else "??:??"


def _format_teacher_names(teachers):
    names = [teacher.get("name") or teacher.get("email") for teacher in teachers if teacher]
    return ", ".join(filter(None, names)) or "Unknown"


def _format_email_cell(value):
    if value == "Unknown":
        return '<strong style="color:#d00000;">Unknown</strong>'
    return html.escape(value)


def _has_missing_teacher(class_info):
    return "Unknown" in (class_info["teacher"], class_info["replacement"])


def _admin_row_style(class_info):
    style = "padding:8px;border-bottom:1px solid #ddd;"
    if _has_missing_teacher(class_info):
        style += "color:#d00000;font-weight:bold;"
    return style


def _send_html_email(recipients, subject, body):
    msg = MIMEMultipart()
    msg["From"] = GMAIL_SENDER
    msg["Reply-to"] = GMAIL_REPLY_TO
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.attach(MIMEText(body + html_signature(), "html"))

    server = create_smtp_transport()
    try:
        server.sendmail(GMAIL_SENDER, recipients, msg.as_string())
    finally:
        server.quit()


def get_daily_classes_recipients():
    return [
        email.strip()
        for email in (DAILY_CLASSES_EMAIL_TO or "").split(";")
        if email.strip()
    ]


def _teacher_name(teacher):
    return (teacher or {}).get("Full_Name__c") or (teacher or {}).get("Email__c") or "Unknown"


def _replacement_teacher_name(replacement):
    return _teacher_name((replacement or {}).get("Teacher__r"))


def _replacement_date(replacement):
    return dt.datetime.strptime(replacement.get("Date__c"), "%Y-%m-%d").date()


def get_replacement_note(class_data, target_date):
    replacements = (class_data.get("Replacements__r") or {}).get("records", [])
    replacements = [replacement for replacement in replacements if replacement.get("Date__c")]
    replacements = sorted(replacements, key=_replacement_date)

    current_teacher = _teacher_name(class_data.get("Teacher__r"))
    permanent_replacement_today = None
    replaced_by_permanent_today = None

    for replacement in replacements:
        replacement_date = _replacement_date(replacement)
        if replacement.get("RecordTypeId") != PERMANENT_REPLACEMENT_TYPE_ID or replacement_date > target_date:
            continue

        if replacement_date == target_date:
            permanent_replacement_today = replacement
            replaced_by_permanent_today = current_teacher

        current_teacher = _replacement_teacher_name(replacement)

    one_time_replacements_today = [
        replacement
        for replacement in replacements
        if replacement.get("RecordTypeId") == ONE_TIME_REPLACEMENT_TYPE_ID
        and _replacement_date(replacement) == target_date
    ]
    if one_time_replacements_today:
        return f"Replaces {current_teacher} (OneTime)"

    if permanent_replacement_today:
        return f"Replaces {replaced_by_permanent_today} (Permanent)"

    return ""


def get_classes_for_date(target_date):
    sf = getSF()
    day_of_week = target_date.strftime("%A")
    date_value = target_date.isoformat()

    results = sf.sf.query_all_iter(f"""
        SELECT
            Id, Code__c, Start_Time__c, End_Time__c, Day_of_Week__c,
            Account.Name,
            Teacher__r.Email__c, Teacher__r.Full_Name__c,
            Additional_Invite__c,
            Yearly_Schedule__r.Start_Date__c,
            Yearly_Schedule__r.End_Date__c,
            Yearly_Schedule__r.Associated_Calendar__r.Holiday_Weeks__c,
            Yearly_Schedule__r.Associated_Calendar__r.Holiday_Days__c,
            Yearly_Schedule__r.Overwrite_Cancelled__c,
            Overwrite_Cancelled__c,
            (
                SELECT
                    Teacher__r.Email__c, Teacher__r.Full_Name__c,
                    Date__c, RecordTypeId
                FROM Replacements__r
                WHERE Deleted__c = False
            )
        FROM Opportunity
        WHERE RecordTypeId = '012060000003OPWAA2'
            AND StageName != 'Cancelled'
            AND Day_of_Week__c = '{day_of_week}'
            AND Yearly_Schedule__r.Start_Date__c <= {date_value}
            AND Yearly_Schedule__r.End_Date__c >= {date_value}
    """)

    classes = []
    for class_data in results:
        schedule = getSchedule(class_data)
        teachers = schedule.get(target_date)
        if teachers is None:
            continue

        classes.append({
            "code": class_data.get("Code__c") or "Unknown",
            "school_name": (class_data.get("Account") or {}).get("Name") or "Unknown",
            "start_time": _format_time(class_data.get("Start_Time__c")),
            "end_time": _format_time(class_data.get("End_Time__c")),
            "teachers": teachers,
            "teacher": _format_teacher_names(teachers),
            "replacement": get_replacement_note(class_data, target_date),
        })

    return sorted(classes, key=lambda class_info: (class_info["start_time"], class_info["code"]))


def build_daily_classes_email(classes, target_date):
    formatted_date = target_date.strftime("%A %d/%m/%Y")
    rows = "".join(
        f"""
        <tr>
            <td style="{_admin_row_style(class_info)}">{html.escape(class_info["code"])}</td>
            <td style="{_admin_row_style(class_info)}">{html.escape(class_info["start_time"])}</td>
            <td style="{_admin_row_style(class_info)}">{html.escape(class_info["end_time"])}</td>
            <td style="{_admin_row_style(class_info)}">{_format_email_cell(class_info["teacher"])}</td>
            <td style="{_admin_row_style(class_info)}">{_format_email_cell(class_info["replacement"])}</td>
        </tr>
        """
        for class_info in classes
    )

    if not rows:
        rows = """
        <tr>
            <td colspan="5" style="padding:8px;border-bottom:1px solid #ddd;">No classes today.</td>
        </tr>
        """

    return f"""
    <p>Classes taking place today ({html.escape(formatted_date)}):</p>
    <table style="border-collapse:collapse;width:100%;max-width:720px;">
        <thead>
            <tr>
                <th align="left" style="padding:8px;border-bottom:2px solid #333;">Code</th>
                <th align="left" style="padding:8px;border-bottom:2px solid #333;">Start</th>
                <th align="left" style="padding:8px;border-bottom:2px solid #333;">End</th>
                <th align="left" style="padding:8px;border-bottom:2px solid #333;">Teacher</th>
                <th align="left" style="padding:8px;border-bottom:2px solid #333;">Replacement</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    """


def send_daily_classes_email(target_date=None):
    recipients = get_daily_classes_recipients()
    if not recipients:
        raise ValueError("DAILY_CLASSES_EMAIL_TO is not set in config.env")

    target_date = target_date or dt.datetime.now(LOCAL_TIMEZONE).date()
    classes = get_classes_for_date(target_date)
    body = build_daily_classes_email(classes, target_date)
    subject_prefix = "[MISSING TEACHER] " if any(_has_missing_teacher(class_info) for class_info in classes) else ""
    subject = f"{subject_prefix}Classes today - {target_date.strftime('%d/%m/%Y')}"

    _send_html_email(recipients, subject, body)
    print(f"[SUCCESS] Daily classes email sent to {', '.join(recipients)}")

    return {
        "date": target_date.isoformat(),
        "recipients": recipients,
        "class_count": len(classes),
    }


def parse_target_date(argv=None, script_name="scripts/send_daily_classes_email.py"):
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        return None

    try:
        return dt.datetime.strptime(argv[0], "%Y-%m-%d").date()
    except ValueError as exc:
        raise SystemExit(f"Usage: python {script_name} [YYYY-MM-DD]") from exc


def main(argv=None):
    result = send_daily_classes_email(parse_target_date(argv))
    print(result)


@scheduler_fn.on_schedule(
    schedule="0 5 * * *",
    timezone=scheduler_fn.Timezone("Europe/Brussels"),
    region="europe-west1",
    timeout_sec=540,
    memory=options.MemoryOption.MB_512,
)
def daily_classes_email(event: scheduler_fn.ScheduledEvent) -> None:
    send_daily_classes_email()
