from Helpers import firebase_functions_custom, https_fn_custom, deleter

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def additional_a_delete(data):
    return deleter("Replacement__c", data.get("details", {}).get("Id"))
