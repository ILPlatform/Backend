def safe_create(object, details):
    valid_fields = {field['name'] for field in object.describe()['fields']}
    valid_details = {key: value for key, value in details.items() if key in valid_fields}
    return object.create(valid_details)

def safe_delete(object, id):
    try:
        object.update(id, {"Deleted__c": True})
    except Exception as e:
        return {"data": {"response": f"Error deleting replacement: {e}", "status": 400}}

    return {"data": {"response": "Success", "status": 200}}
