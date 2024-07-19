# from dotenv.main import load_dotenv
from simple_salesforce import Salesforce
from pprint import pprint
from firebase_functions.params import StringParam
from firebase_functions import logger

class SFConnector:
    def __init__(self, SF_USERNAME, SF_PASSWORD, SF_SECURITY_TOKEN, SF_DOMAIN):
        logger.log(f"[LOG] Initializing Salesforce client {SF_USERNAME}")
        if SF_DOMAIN:
            self.sf = Salesforce(
                username=SF_USERNAME,
                password=SF_PASSWORD,
                security_token=SF_SECURITY_TOKEN,
                domain="test")
        else:
            self.sf = Salesforce(
                username=SF_USERNAME,
                password=SF_PASSWORD,
                security_token=SF_SECURITY_TOKEN)

    def update_opportunity(self, id, data):
        return self.sf.Opportunity.update(id, data)

    def update_picklist(self, id, data):
        return self.sf.Picklist__c.update(id, data)
