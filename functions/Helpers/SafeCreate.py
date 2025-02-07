def safe_create(object, details):
    valid_fields = {field['name'] for field in object.describe()['fields']}
    valid_details = {key: value for key, value in details.items() if key in valid_fields}
    return object.create(valid_details)
