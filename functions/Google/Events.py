from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import re

# Global Variables
CALENDAR_CLASSES_ID = os.getenv('CALENDAR_CLASSES_ID')
CALENDAR_CAMPS_ID = os.getenv('CALENDAR_CAMPS_ID')

class Events():
    CALENDAR_CLASSES_ID = os.getenv('CALENDAR_CLASSES_ID')
    CALENDAR_CAMPS_ID = os.getenv('CALENDAR_CAMPS_ID')

    def __init__(self, Client, year, month, blacklist):
        self.Client = Client
        self.year = year
        self.month = month
        self.blacklist = [*blacklist, CALENDAR_CLASSES_ID, CALENDAR_CAMPS_ID]

    def get_events(self, sf):
        # Get First and Last Day of Month
        first_day = datetime(self.year, self.month, 1).isoformat()
        last_day = (datetime(self.year, self.month, 1) + relativedelta(months=1, days=0)).isoformat()

        # Get Classes Events
        events_classes_result = self.Client.calendar.events().list(
            calendarId=CALENDAR_CLASSES_ID,
            timeMin=first_day + 'Z',
            timeMax=last_day + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events_classes = events_classes_result.get('items', [])
        events_classes = self.__process_google_events([event for event in events_classes if 'start' in event and 'dateTime' in event['start']])

        # Get Camp Events
        events_camps_result = self.Client.calendar.events().list(
            calendarId=CALENDAR_CAMPS_ID,
            timeMin=first_day + 'Z',
            timeMax=last_day + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events_camps = events_camps_result.get('items', [])
        events_camps = self.__process_google_events([event for event in events_camps if 'start' in event and 'dateTime' in event['start']])

        # Get Additional Payments from SF
        events_extra = sf.get_additional_payments(self.year, self.month)

        # Combine Events
        events = events_classes + events_camps + events_extra

        # Process Events
        return events

    def __process_google_events(self, events):
        processed_events = []
        for event in events:
            not_match_list = lambda email: not any([re.compile(black).match(email) for black in self.blacklist])
            try:
                teachers = [attendee.get('email') for attendee in event.get('attendees') if not_match_list(attendee.get('email'))] if event.get('attendees') else []
                start = event['start']['dateTime']
                end = event['end']['dateTime']
                minutes = (datetime.fromisoformat(end) - datetime.fromisoformat(start)).total_seconds() / 60
                minutes = round(minutes, 2)
                start = start[:10]
                code = event['summary'].split(' - ')[0].replace(' ', '')
                held = not('[' in code and ']' in code)
                if ']' in code:
                    code = code.split(']')[1]
                title = event['summary'].split(' - ')
                title.pop(0)
                title = '-'.join(title)
                amount = round(self.__calculate_amount(code, minutes), 2)
                nice_name = f"    [{code}] {title} ({start}, {minutes}min, {amount}€)"
                processed_events.append({
                    'teachers': teachers,
                    'held': held,
                    'minutes': minutes,
                    'amount': amount,
                    'nice_name': nice_name
                })
            except Exception as e:
                raise KeyError(f"[WARNING] - Problem with event {event.get('summary')} -> {e}")
        return processed_events

    @staticmethod
    def __calculate_amount(code, timespan):
        price_per_minute = {
            'A': 17 / 60,
            'E': 0 / 60,
            'C': 17 / 60,
            'P': 20 / 60,
            'O': 12 / 60,
            'S': 15 / 60
        }
        if not code[0] or code[0] not in price_per_minute:
            raise ValueError(f"ERROR - Code `{code}` not correct!")
        return price_per_minute[code[0]] * timespan
