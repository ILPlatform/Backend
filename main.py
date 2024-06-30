from Salesforce.SFProcessor import SFProcessor
from Google.GoogleConnector import GoogleConnector
from Actions.CampsEvents import update_and_create_camps_per_week
from Actions.CampsForm import create_camps_form
import pick

from dotenv import load_dotenv
load_dotenv()
from pprint import pprint

sf = SFProcessor()
google = GoogleConnector()

title = "Select your action"
options = [
    "Get Teachers for Partners",
    "Create Camps for a Week",
    "Create Camps Form"
]

option, index = pick.pick(options, title)

if index == 0:
    partner = input("Enter the Partner: ")
    print("\n".join(sf.get_teachers_for_partners(partner)))
elif index == 1:
    week_codes = map(lambda x: x["code"], sf.get_camp_weeks())
    print(f"Possible Week Codes are {', '.join(week_codes)}")
    week_code = input("Enter the Week Code: ")
    update_and_create_camps_per_week(google, sf, week_code)
elif index == 2:
    title = input("Enter the Form Title: ")
    week_codes = input("Enter the Week Codes: ").replace(" ", "").split(",")
    create_camps_form(google, sf, title, week_codes)
