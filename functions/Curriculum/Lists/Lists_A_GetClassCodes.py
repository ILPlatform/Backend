from Helpers import getter

lists_a_get_class_codes = getter(lambda data: """
    SELECT Id, Code__c , Day_of_Week__c, Start_Time__c, End_Time__c, Account.Name
    FROM Opportunity
    """, auth_level=2)
