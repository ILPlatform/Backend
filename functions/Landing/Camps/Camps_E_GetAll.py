# Function to get all documents related to an authenticated user. Requires authentication.

from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import firestore, auth
from Salesforce import getSF
from Emails import send_email_user
import json

@https_fn_custom(access=True)
@firebase_functions_custom(auth_level=0)
def camps_e_get_all(data):
    # Initialize DB and SF
    sf = getSF()

    # Salesforce SOQL query
    response = sf.sf.query_all(f'''
    SELECT
        Id, Name, Start_Date__c, End_Date__c, Number_of_Days__c, Excluded_Day__c,
        (
            SELECT
                Id, Account.Name, Price__c, Registration_Link__c, Ages_Announced__c,
                Parent_Organisation_Name__c,
                Account.BillingAddress
            FROM Opportunities__r
        )
    FROM Picklist__c
    WHERE RecordTypeId = '012P5000001CUEfIAO'
    ''')

    print(response)

    # Function to format Salesforce data into the required JSON structure
    def format_camps_data(records):
        formatted_data = {}

        for record in records:
            period_key = f"{record['Id']}_{record['Start_Date__c'][:4]}"  # Create a unique period key
            camps = []

            # Check if Opportunities__r exists and has records
            opportunities = record.get('Opportunities__r')
            if opportunities and opportunities.get('records'):
                for opp in opportunities['records']:
                    if not opp.get("Registration_Link__c") or not opp.get("Price__c"):
                        continue
                    camp = {
                        "title": opp.get("Title", "sportgames"),
                        "age": opp.get("Ages_Announced__c"),
                        "partner": opp.get("Parent_Organisation_Name__c"),
                        "school": opp["Account"]["Name"] if opp.get("Account") else None,
                        "price": f"{int(opp['Price__c'])}€",
                        "register": opp['Registration_Link__c'],
                        "address": f"{opp['Account']['BillingAddress']['street']}, {opp['Account']['BillingAddress']['postalCode']} {opp['Account']['BillingAddress']['city']}, {opp['Account']['BillingAddress']['country']}" if opp.get("Account").get("BillingAddress") else None
                    }
                    camps.append(camp)

            formatted_data[period_key] = {
                "period": period_key,
                "name": record.get('Name', "N/A"),
                "start": record.get('Start_Date__c', "N/A"),
                "end": record.get('End_Date__c', "N/A"),
                "days": int(record.get('Number_of_Days__c', 5)),
                "not": record.get('Excluded_Day__c', "N/A"),
                "camps": camps
            }

            # Print the formatted data for the current record
            print(json.dumps(formatted_data[period_key], indent=4))

        return formatted_data

    # Retrieve and format the data
    records = response['records']
    formatted_data = format_camps_data(records)

    # # Output the data to a JSON file
    # with open('formatted_camps_data.json', 'w') as f:
    #     json.dump(formatted_data, f, indent=4)

    return {"data": { "response": formatted_data, "status": 200}}
