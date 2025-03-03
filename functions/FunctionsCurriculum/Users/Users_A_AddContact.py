from Helpers import firebase_functions_custom, https_fn_custom, getter
from Google.Connector import GoogleConnector

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def users_a_add_contact(data):
    google_token = data.get("user_details", {}).get("google_oauth")
    if not google_token:
        return {"data": {"response": "Invalid Google token", "status": 401}}

    contact_details = getter(f"""
        SELECT Name, Last_Name__c, Full_Name__c, Email__c, Phone__c, Other_Phone__c
        FROM Employee__c
        WHERE Id='{data.get("details", {}).get("Id")}'
        """).get("data", {}).get("response", {})[0]

    google = GoogleConnector(google_token)
    contacts = google.contacts

    contact = {
        "names": [{
            "givenName": contact_details.get("Name"),
            "familyName": contact_details.get("Last_Name__c")
        }],
        "emailAddresses": [{"value": contact_details.get("Email__c")}],
        "phoneNumbers": [
            {
                "value": contact_details.get("Phone__c"),
                "type": "mobile"
            },
            {
                "value": contact_details.get("Other_Phone__c"),
                "type": "home"
            }
        ],
        "organizations": [{
            "name": "ILPlatform",
            "title": "Enseignant"
        }]
    }

    contacts.people().createContact(body=contact).execute()
    return {"data": {"response": "Success", "status": 200}}
