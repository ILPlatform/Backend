from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def replacements_a_solve(data):
    # Get parameters
    details = data.get("details")
    print(details)
    # Initialize the Salesforce client
    sf = getSF()

    # Update the replacement
    sf.sf.Replacement__c.update(details.get("Id"),
        { "Teacher__c": details.get("Teacher__r", {}).get("Id") if details.get("Teacher__r", {}) else None })

    return {"data": {"response": "Success", "status": 200}}
