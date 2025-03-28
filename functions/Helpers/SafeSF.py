def safe_create(object, details):
    valid_fields = {field['name'] for field in object.describe()['fields']}
    valid_details = {key: value for key, value in details.items() if key in valid_fields}
    return object.create(valid_details)

def safe_update(object, details):
    valid_fields = {field['name'] for field in object.describe()['fields'] if field['name'] != "Id"}
    valid_details = {key: value for key, value in details.items() if key in valid_fields}
    return object.update(details.get("Id"), valid_details)

def safe_delete(object, id):
    try:
        object.update(id, {"Deleted__c": True})
    except Exception as e:
        return {"data": {"response": f"Error deleting replacement: {e}", "status": 400}}

    return {"data": {"response": "Success", "status": 200}}

def safe_query(sf, unsafe_query):
    results = []
    offset = 0
    while True:
        safe_query = f"{unsafe_query} LIMIT 200 OFFSET {offset}"
        response = sf.sf.query(safe_query)
        records = response.get('records', [])
        results.extend(records)

        if len(list(records)) == 200:
            offset += 200
        else:
            break
    return results
