from Helpers import firebase_functions_custom, https_fn_custom, safe_delete
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=10)
def additional_payments_a_delete(data):
    # Initialize DB and SF
    sf = getSF()

    # Retrieve the payment details
    payment = data.get("details")
    if not payment or not payment.get("Id"):
        return {"data": {"response": "Payment details are required", "status": 400}}

    # Delete the payment
    safe_delete(sf.sf.Payment__c, payment.get("Id"))

    # Return the response
    return {"data": {"response": "Success", "status": 200}}
