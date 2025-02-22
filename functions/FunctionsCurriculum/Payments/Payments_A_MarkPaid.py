from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=10)
def payments_a_mark_paid(data):
    # Initialize DB and SF
    sf = getSF()

    # Get the parameters
    payment_id = data.get("payment_id")

    # Update the payment in SF
    if data.get("reverse"):
        sf.sf.Payment__c.update(payment_id, {"Paid__c": False})
    else:
        sf.sf.Payment__c.update(payment_id, {"Paid__c": True})

    return {"data": {"response": 1, "status": 200}}
