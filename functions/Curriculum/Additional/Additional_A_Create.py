from Helpers import firebase_functions_custom, https_fn_custom, creator

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def additional_a_create(data):
    return creator("Replacement__c", data.get("details"), "012P5000001YwypIAC")
