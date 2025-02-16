from Helpers import firebase_functions_custom, https_fn_custom, safe_query, safe_delete
from Salesforce import getSF

def getter(query, auth_level):
    # Define API function
    @https_fn_custom()
    @firebase_functions_custom(auth_level=auth_level)
    def get(data):
        # Initialize DB and SF
        sf = getSF()

        # Get response from SF
        results = safe_query(sf, query(data))

        # Return response
        return {"data": {"response": results, "status": 200}}

    return get

def deleter(object_name, auth_level):
    # Define API function
    @https_fn_custom()
    @firebase_functions_custom(auth_level=auth_level)
    def delete(data):
        # Initialize the Salesforce client
        sf = getSF()

        # Delete the object
        details = data.get("details")
        object_api = getattr(sf.sf, object_name)
        return safe_delete(object_api, details.get("Id"))

    return delete
