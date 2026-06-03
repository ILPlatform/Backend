import datetime as dt
import html
from collections import defaultdict

from firebase_functions import options, scheduler_fn

from .DailyClassesEmail import (
    LOCAL_TIMEZONE,
    _send_html_email,
    get_classes_for_date,
    parse_target_date,
)


FRENCH_DAYS = {
    0: "Lundi",
    1: "Mardi",
    2: "Mercredi",
    3: "Jeudi",
    4: "Vendredi",
    5: "Samedi",
    6: "Dimanche",
}

FRENCH_MONTHS = {
    1: "janvier",
    2: "février",
    3: "mars",
    4: "avril",
    5: "mai",
    6: "juin",
    7: "juillet",
    8: "août",
    9: "septembre",
    10: "octobre",
    11: "novembre",
    12: "décembre",
}


def _teacher_display_name(teacher):
    return (teacher or {}).get("name") or (teacher or {}).get("email") or "Teacher"


def _format_french_date(date):
    return f"{FRENCH_DAYS[date.weekday()]} {date.day} {FRENCH_MONTHS[date.month]} {date.year}"


def _arrival_time(start_time):
    if start_time == "??:??":
        return start_time

    parsed_time = dt.datetime.strptime(start_time, "%H:%M")
    return (parsed_time - dt.timedelta(minutes=15)).strftime("%H:%M")


def group_classes_by_teacher(classes):
    grouped_classes = defaultdict(lambda: {"name": "Teacher", "classes": []})

    for class_info in classes:
        for teacher in class_info.get("teachers", []):
            email = (teacher or {}).get("email")
            if not email:
                continue

            grouped_classes[email]["name"] = _teacher_display_name(teacher)
            grouped_classes[email]["classes"].append(class_info)

    return dict(grouped_classes)


def build_teacher_classes_email(classes, target_date, teacher_name):
    formatted_date = _format_french_date(target_date)
    rows = "".join(
        f"""
        <tr>
            <td style="padding:8px;border-bottom:1px solid #ddd;">{html.escape(class_info["code"])}</td>
            <td style="padding:8px;border-bottom:1px solid #ddd;">{html.escape(class_info["school_name"])}</td>
            <td style="padding:8px;border-bottom:1px solid #ddd;">{html.escape(_arrival_time(class_info["start_time"]))} - {html.escape(class_info["end_time"])}</td>
        </tr>
        """
        for class_info in classes
    )

    return f"""
    <p>Bonjour {html.escape(teacher_name)},</p>
    <p>Voici tes cours pour aujourd'hui ({html.escape(formatted_date)}):</p>
    <table style="border-collapse:collapse;width:100%;max-width:720px;">
        <thead>
            <tr>
                <th align="left" style="padding:8px;border-bottom:2px solid #333;">Code</th>
                <th align="left" style="padding:8px;border-bottom:2px solid #333;">École</th>
                <th align="left" style="padding:8px;border-bottom:2px solid #333;">Horaire</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    <p><strong>Il y a une erreur?</strong> Dans le cas d'une erreur, nous n'avons pas correctement noté ton absence, même si tu nous l'as communiquée. Dans le cas d'une erreur, merci de contacter Daniel (<a href="tel:+32470877429">+32 470 87 74 29</a>) et Eimantas (<a href="tel:+32456194405">+32 456 19 44 05</a>) <strong>immédiatement</strong>.</p>
    <p>Merci pour ton aide!</p>
    """


def send_daily_teacher_classes_emails(target_date=None):
    target_date = target_date or dt.datetime.now(LOCAL_TIMEZONE).date()
    classes = get_classes_for_date(target_date)
    grouped_classes = group_classes_by_teacher(classes)
    subject = f"Cours du {_format_french_date(target_date)}"
    sent = []

    for email, teacher_data in sorted(grouped_classes.items()):
        teacher_classes = sorted(
            teacher_data["classes"],
            key=lambda class_info: (class_info["start_time"], class_info["code"]),
        )
        body = build_teacher_classes_email(teacher_classes, target_date, teacher_data["name"])
        _send_html_email([email], subject, body)
        sent.append({"email": email, "class_count": len(teacher_classes)})
        print(f"[SUCCESS] Daily teacher classes email sent to {email}")

    return {
        "date": target_date.isoformat(),
        "teacher_count": len(sent),
        "sent": sent,
    }


def main(argv=None):
    result = send_daily_teacher_classes_emails(
        parse_target_date(argv, "scripts/send_daily_teacher_classes_email.py")
    )
    print(result)


@scheduler_fn.on_schedule(
    schedule="0 6 * * *",
    timezone=scheduler_fn.Timezone("Europe/Brussels"),
    region="europe-west1",
    timeout_sec=540,
    memory=options.MemoryOption.MB_512,
)
def daily_teacher_classes_email(event: scheduler_fn.ScheduledEvent) -> None:
    send_daily_teacher_classes_emails()
