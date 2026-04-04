# from dotenv.main import load_dotenv
from simple_salesforce import Salesforce
from Logger import log

class SFConnector:
    def __init__(self, SF_USERNAME, SF_PASSWORD, SF_SECURITY_TOKEN, SF_DOMAIN):
        try:
            if SF_DOMAIN:
                self.sf = Salesforce(
                    username=SF_USERNAME,
                    password=SF_PASSWORD,
                    security_token=SF_SECURITY_TOKEN,
                    domain=SF_DOMAIN)
            else:
                self.sf = Salesforce(
                    username=SF_USERNAME,
                    password=SF_PASSWORD,
                    security_token=SF_SECURITY_TOKEN)
        except Exception as e:
            log("ERROR", "Salesforce", f"Authentication failed: {e}")
            raise ValueError(f"[ERROR] Could not authenticate to Salesforce client {SF_USERNAME} -> {e}")
        log("AUTHENTICATE", "Salesforce", f"Connected to {SF_USERNAME}")

    def update_opportunity(self, id, data):
        return self.sf.Opportunity.update(id, data)
