from Helpers import getter

interviews_a_get_all = getter(lambda data: """
    SELECT FIELDS(ALL)
    FROM Note__c
    WHERE RecordTypeId = '012P5000001UtMf'
    """, auth_level=3)
