# Function to get all the documents from the database. Requires document admin level.

from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import auth, firestore
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=3)
def interviews_a_get_all(data):
    # Initialize DB and SF
    sf = getSF()

    # Get all contracts
    interviews = sf.sf.query_all_iter(f"""
        SELECT
            Id, Date_Time__c, Name__c, Email__c
        FROM Note__c
        WHERE RecordTypeId = '012P5000001UtMf'
        """)

    return {"data": {"response": list(interviews), "status": 200}}
