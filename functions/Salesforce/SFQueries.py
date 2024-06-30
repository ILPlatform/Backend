
class SFQueries:
    WEEK_RECORD_TYPE_ID = '012P5000001CUEfIAO'

    def __init__(self):
        pass

    def get_camp_details(self, code):
        query = f"""
            SELECT Teacher__r.Email, Week__r.Start_Date__c, Account.Name, Account.BillingAddress, Ages_Real__c, Time_Schedule__r.Start_Pay_Time__c, Time_Schedule__r.End_Pay_Time__c, Time_Schedule__r.Description__c, Description, Id, Google_Event__c, Time_Schedule__r.Name
            FROM Opportunity
            WHERE Camp_Code__c='{code}'
            """
        return query

    def get_camp_weeks(self):
        query = f"""
            SELECT Name, Start_Date__c, End_Date__c, Number_of_Days__c, Week_Code__c
            FROM Picklist__c
            WHERE RecordTypeId='{self.WEEK_RECORD_TYPE_ID}'
            ORDER BY Start_Date__c
            """
        return query

    def get_camps_per_week(self, week_code, confirmed=True):
        conf_query = "AND StageName='Confirmed'"
        query = f"""
            SELECT Camp_Code__c
            FROM Opportunity
            WHERE Week__r.Week_Code__c='{week_code}' {conf_query if confirmed else ''}
            ORDER BY Time_Schedule__r.Name DESC, Account.Name ASC
            """
        return query

    def get_possible_camps_per_week(self, week_code):
        query = f"""
            SELECT Camp_Code__c
            FROM Opportunity
            WHERE Week__r.Week_Code__c='{week_code}' AND StageName!='Cancelled'
            ORDER BY Time_Schedule__r.Name DESC, Account.Name ASC
            """
        return query

    def get_teachers_for_partners(self, partner, only_confirmed):
        confirmed_query =  "AND StageName='Confirmed'" if only_confirmed else ""
        query = f"""
            SELECT Week__r.Name, Account.Name, Teacher__r.Name, Teacher__r.Phone, Partner_Organisation__c, Time_Schedule__r.Name
            FROM Opportunity
            WHERE Partner_Organisation__c LIKE '%{partner}%' {confirmed_query}
            ORDER BY Week__r.Name ASC, Account.Name ASC, Time_Schedule__r.Name DESC
            """
        return query

    def get_week_name(self, week_code):
        query = f"""
            SELECT Name, Start_Date__c, End_Date__c
            FROM Picklist__c
            WHERE Week_Code__c='{week_code}'
            """
        return query
