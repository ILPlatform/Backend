import datetime as dt

def getEventDict(details, course_days):
    return {
        'summary': f'{details["Code__c"]} - {details["Account"]["Name"]} [{details["Ages_Announced__c"] if details.get("Ages_Announced__c") and details.get("Ages_Announced__c") != "" else "???"}]',
        'location': f"""
            {details["Account"]["BillingAddress"]["street"]},
            {details["Account"]["BillingAddress"]["postalCode"]}
            {details["Account"]["BillingAddress"]["city"]},
            {details["Account"]["BillingAddress"]["country"]}""",
        'description':
            f"Horaire de cours: {details['Start_Time__c'][:5]} - {details['End_Time__c'][:5]}. " + \
            "Arrivée attendue 15 minutes avant pour préparer la salle.\n\n" + \
            f"Procédure de présences: {details['Yearly_Schedule__r']['Attendance_Description__c']}",
        'start': {
            'dateTime': (dt.datetime.combine(
                course_days[0],
                dt.datetime.strptime(details["Start_Time__c"][:-1], "%H:%M:%S.%f").time()
            )-(dt.timedelta(minutes=15) if not details["Account"]["Online__c"] else dt.timedelta(0))).isoformat(),
            'timeZone': 'Europe/Brussels',
        },
        'end': {
            'dateTime': dt.datetime.combine(
                course_days[0],
                dt.datetime.strptime(details["End_Time__c"][:-1], "%H:%M:%S.%f").time()
            ).isoformat(),
            'timeZone': 'Europe/Brussels',
        },
        'recurrence': [
            f'RRULE:FREQ=WEEKLY;UNTIL={details["Yearly_Schedule__r"]["End_Date__c"].replace("-", "")}T235959Z'
        ],
        'attendees': [
            {'email': details["Teacher__r"]["Email__c"]} if details.get("Teacher__r") else None,
            {'email': details["Additional_Invite__c"]} if details.get("Additional_Invite__c") else None
        ],
        "conferenceData": {
            "createRequest": {
                "conferenceSolutionKey": { "type": "hangoutsMeet" },
                "requestId": details["Code__c"],
            }
        } if details["Account"]["Online__c"] else None,
        'sendUpdates': 'all'
    }
