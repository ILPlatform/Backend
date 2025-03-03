from Helpers import firebase_functions_custom, https_fn_custom, getter

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def lists_a_get_week_codes(data):
    return getter("""
        SELECT Id, Name, Start_Date__c, End_Date__c, Number_of_Days__c, Week_Code__c
        FROM Picklist__c
        WHERE RecordTypeId='012P5000001CUEfIAO'
        ORDER BY Start_Date__c
    """)
