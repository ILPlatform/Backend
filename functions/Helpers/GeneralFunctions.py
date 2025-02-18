from Helpers import firebase_functions_custom, https_fn_custom, safe_query, safe_delete
from Salesforce import getSF

def getter(query):
    # Initialize DB and SF
    sf = getSF()

    # Get response from SF
    results = safe_query(sf, query)

    # Return response
    return {"data": {"response": results, "status": 200}}

def deleter(object_name, object_id):
    # Initialize the Salesforce client
    sf = getSF()

    # Delete the object
    object_api = getattr(sf.sf, object_name)
    return safe_delete(object_api, object_id)
