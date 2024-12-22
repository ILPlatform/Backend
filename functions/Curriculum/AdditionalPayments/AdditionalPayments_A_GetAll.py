from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import auth
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=10)
def additional_payments_a_get_all(data):
    # Initialize DB and SF
    sf = getSF()

    # Get all payments from SF
    sf_results = list(sf.sf.query_all_iter(f"""
        SELECT
            Id, Name, Amount__c, Year__c, Month__c,
            Beneficiary__r.Id, Beneficiary__r.Full_Name__c,
            CreatedDate
        FROM Payment__c
        WHERE (RecordTypeId = '012P5000001tcX7IAI' OR RecordTypeId = NULL)
            AND Deleted__c = False
    """))

    # Process the results
    results = [
        {
            "id": payment.get("Id"),
            "amount": payment.get("Amount__c"),
            "year": payment.get("Year__c"),
            "month": payment.get("Month__c"),
            "description": payment.get("Name"),
            "beneficiary_id": payment.get("Beneficiary__r").get("Id"),
            "beneficiary_name": payment.get("Beneficiary__r").get("Full_Name__c"),
            "created_date": payment.get("CreatedDate")
        } for payment in sf_results
    ]

    return {"data": {"response": results, "status": 200}}
