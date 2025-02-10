from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=3)
def docs_a_delete(data):
    # Initialize SF
    sf = getSF()

    # Get the parameters
    document = data.get('details')
    if not document or not document.get("Id"):
        return {"data": {"response": "Document ID is required", "status": 400}}

    # Update the document in the database
    sf.sf.Document__c.update(document.get("Id"), {"Deleted__c": True})

    # Retrieve all attached payment objects
    payments = sf.sf.query_all_iter(f"""
        SELECT Id
        FROM Payment__c
        WHERE Document__c = '{document.get("Id")}'
    """)

    # Mark all payments attached as deleted
    for payment in payments:
        sf.sf.Payment__c.update(payment.get("Id"), {"Deleted__c": True})

    return {"data": {"response": "Success", "status": 200}}
