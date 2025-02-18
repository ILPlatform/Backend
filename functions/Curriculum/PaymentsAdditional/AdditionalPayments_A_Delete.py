from Helpers import deleter
from Helpers import https_fn_custom, firebase_functions_custom

@https_fn_custom()
@firebase_functions_custom(auth_level=10)
def additional_payments_a_delete(data):
    return deleter("Payment__c", data.get("details", {}).get("Id"))
