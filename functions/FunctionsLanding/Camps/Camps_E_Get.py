from Helpers import firebase_functions_custom, https_fn_custom, getter

@https_fn_custom(access=True)
@firebase_functions_custom(auth_level=0)
def camps_e_get(data):
    return getter('''
    SELECT
        Id, Name, Start_Date__c, End_Date__c, Number_of_Days__c, Excluded_Day__c,
        Image__c,
        (
            SELECT
                Id, Account.Name, Price__c, Registration_Link__c, Ages_Announced__c,
                Parent_Organisation_Name__c,
                Account.BillingAddress, Partner_Type__c
            FROM Opportunities__r
        )
    FROM Picklist__c
    WHERE RecordTypeId = '012P5000001CUEfIAO'
    ''')
