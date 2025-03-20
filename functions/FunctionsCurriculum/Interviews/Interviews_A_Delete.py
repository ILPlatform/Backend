from Helpers import deleter
from Helpers import https_fn_custom, firebase_functions_custom

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def interviews_a_delete(data):
    return deleter("Note__c", data.get("details", {}).get("Id"))
