from Salesforce.SFProcessor import SFProcessor
import os

# Secret parameters
SF_USERNAME = os.getenv("SF_USERNAME")
SF_PASSWORD = os.getenv("SF_PASSWORD")
SF_SECURITY_TOKEN = os.getenv("SF_SECURITY_TOKEN")

def getSF():
    return SFProcessor(SF_USERNAME, SF_PASSWORD, SF_SECURITY_TOKEN)
