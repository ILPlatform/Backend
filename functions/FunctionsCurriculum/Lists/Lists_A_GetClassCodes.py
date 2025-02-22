from Helpers import getter
from Helpers import https_fn_custom, firebase_functions_custom

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def lists_a_get_class_codes(data):
    return getter("""
    SELECT Id, Code__c, Day_of_Week__c, Start_Time__c, End_Time__c, Account.Name
    FROM Opportunity
    """)
