from Helpers import safe_query, safe_delete
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

def creator(object_name, details, record_type_id):
    try:
        # Initialize the Salesforce client
        sf = getSF()

        # Get the parameters
        details["RecordTypeId"] = record_type_id

        # Retrieve API object
        object_api = getattr(sf.sf, object_name)

        # Extract valid fields of object
        valid_fields = {field['name'] for field in object_api.describe()['fields']}
        valid_details = {key: value for key, value in details.items() if key in valid_fields}

        # Create the instance
        instance = object_api.create(valid_details)

        # Return the object ID
        return {"data": {"response": {"Id": instance.get("id")}, "status": 200}}
    except Exception as e:
        return {"data": {"response": str(e), "status": 400}}
