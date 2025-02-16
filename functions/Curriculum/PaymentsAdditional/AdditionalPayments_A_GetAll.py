from Helpers import getter

additional_payments_a_get_all = getter(lambda data: """
    SELECT FIELDS(ALL), Beneficiary__r.Full_Name__c
    FROM Payment__c
    WHERE (RecordTypeId = '012P5000001tcX7IAI' OR RecordTypeId = NULL)
        AND Deleted__c = False
    """, auth_level=10)
