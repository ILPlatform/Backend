from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=10)
def payments_a_update(data):
    # Initialize DB and SF
    sf = getSF()

    # Get the parameters
    details = data.get("details")

    # Update the payment in SF
    sf.sf.Payment__c.update(details.get("Id"), {"Amount__c": details.get("Amount__c"), "Updated__c": True})

    return {"data": {"response": 1, "status": 200}}
