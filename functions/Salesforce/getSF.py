from Salesforce.SFProcessor import SFProcessor
from firebase_functions.params import StringParam

# Secret parameters
SF_USERNAME = StringParam("SF_USERNAME")
SF_PASSWORD = StringParam("SF_PASSWORD")
SF_SECURITY_TOKEN = StringParam("SF_SECURITY_TOKEN")

def getSF():
    try:
        return SFProcessor(SF_USERNAME.value, SF_PASSWORD.value, SF_SECURITY_TOKEN.value), "", True
    except Exception as e:
        return None, str(e), False
