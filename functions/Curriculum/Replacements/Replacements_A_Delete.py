from Helpers import firebase_functions_custom, https_fn_custom, safe_delete
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def replacements_a_delete(data):
    # Initialize the Salesforce client
    sf = getSF()

    # Delete the replacement
    details = data.get("details")
    return safe_delete(sf.sf.Replacement__c, details.get("Id"))
