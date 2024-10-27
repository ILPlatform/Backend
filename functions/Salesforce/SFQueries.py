
class SFQueries:
    WEEK_RECORD_TYPE_ID = '012P5000001CUEfIAO'

    def __init__(self):
        pass

    def get_camp_details(self, code):
        query = f"""
            SELECT Name, Camp_Code__c, Teacher__r.Email__c, Week__r.Name, Week__r.Id, Week__r.Start_Date__c, Week__r.End_Date__c, Account.Name, Account.BillingAddress, Ages_Real__c, Time_Schedule__r.Start_Pay_Time__c, Time_Schedule__r.Time_Slot__c ,Time_Schedule__r.End_Pay_Time__c, Time_Schedule__r.Start_Pay_Time_Day_1__c, Time_Schedule__r.Description__c, Description, Id, Google_Event__c, Time_Schedule__r.Name, Google_Drive_Pictures__c, Week__r.Holiday__r.Google_Drive_Pictures_ID__c, Week__r.Holiday__r.Name, Week__r.Holiday__r.Id, Week__r.Google_Drive_Pictures_ID__c, Week__r.Excluded_Day__c,
                (
                    SELECT Id, Teacher__r.Email__c, Date__c
                    FROM Replacements__r
                    WHERE Deleted__c = False
                )
            FROM Opportunity
            WHERE Camp_Code__c='{code}'
            """
        return query

    def get_all_camp_details(self, week_codes):
        query = f"""
            SELECT Name, Camp_Code__c, Teacher__r.Email__c, Week__r.Name, Week__r.Id, Week__r.Start_Date__c, Week__r.End_Date__c, Account.Name, Account.BillingAddress, Ages_Real__c, Time_Schedule__r.Start_Pay_Time__c, Time_Schedule__r.Time_Slot__c ,Time_Schedule__r.End_Pay_Time__c, Time_Schedule__r.Start_Pay_Time_Day_1__c, Time_Schedule__r.Description__c, Description, Id, Google_Event__c, Time_Schedule__r.Name, Google_Drive_Pictures__c, Week__r.Holiday__r.Google_Drive_Pictures_ID__c, Week__r.Holiday__r.Name, Week__r.Holiday__r.Id, Week__r.Google_Drive_Pictures_ID__c, Week__r.Excluded_Day__c,
            Overwrite_Cancelled__c,
                (
                    SELECT Id, Teacher__r.Email__c, Date__c
                    FROM Replacements__r
                    WHERE Deleted__c = False
                )
            FROM Opportunity
            WHERE Week__r.Week_Code__c IN ({','.join(list(map(lambda x: "'" + x + "'", week_codes)))})
                AND StageName='Confirmed'
            """
        return query

    def get_all_class_details(self, year_code):
        query = f"""
        SELECT  Id, Name, Code__c, Teacher__r.Email__c,
                Account.Name, Account.BillingAddress,
                Start_Time__c, End_Time__c, Day_of_Week__c,
                Yearly_Schedule__r.Start_Date__c, Yearly_Schedule__r.End_Date__c,
                Yearly_Schedule__r.Associated_Calendar__r.Holiday_Weeks__c, Yearly_Schedule__r.Associated_Calendar__r.Holiday_Days__c,
                Yearly_Schedule__r.Overwrite_Cancelled__c,
                Overwrite_Cancelled__c, Additional_Invite__c,
                Google_Event__c, Ages_Announced__c,
                (
                    SELECT Teacher__r.Email__c, Date__c, RecordTypeId
                    FROM Replacements__r
                    WHERE Deleted__c = False
                )

        FROM Opportunity
        WHERE Calendar__r.Year_Code__c='{year_code}'
            AND StageName!='Cancelled'
        """
        return query

    def get_all_class_details2(self, week_code):
        query = f"""
        SELECT  Id, Name, Code__c, Teacher__r.Email__c,
                Account.Name, Account.BillingAddress, Account.Online__c,
                Start_Time__c, End_Time__c, Day_of_Week__c,
                Yearly_Schedule__r.Start_Date__c, Yearly_Schedule__r.End_Date__c,
                Yearly_Schedule__r.Associated_Calendar__r.Holiday_Weeks__c, Yearly_Schedule__r.Associated_Calendar__r.Holiday_Days__c,
                Yearly_Schedule__r.Overwrite_Cancelled__c,
                Overwrite_Cancelled__c, Additional_Invite__c,
                Google_Event__c, Ages_Announced__c,
                (
                    SELECT Teacher__r.Email__c, Date__c, RecordTypeId
                    FROM Replacements__r
                    WHERE Deleted__c = False
                )

        FROM Opportunity
        WHERE Code__c='{week_code}'
            AND StageName!='Cancelled'
        """
        return query

    def get_all_class_details3(self, class_id):
        query = f"""
        SELECT  Id, Name, Code__c, Teacher__r.Email__c,
                Account.Name, Account.BillingAddress, Account.Online__c,
                Start_Time__c, End_Time__c, Day_of_Week__c,
                Yearly_Schedule__r.Start_Date__c, Yearly_Schedule__r.End_Date__c,
                Yearly_Schedule__r.Associated_Calendar__r.Holiday_Weeks__c, Yearly_Schedule__r.Associated_Calendar__r.Holiday_Days__c,
                Yearly_Schedule__r.Overwrite_Cancelled__c,
                Overwrite_Cancelled__c, Additional_Invite__c,
                Google_Event__c, Ages_Announced__c,
                (
                    SELECT Teacher__r.Email__c, Date__c, RecordTypeId
                    FROM Replacements__r
                    WHERE Deleted__c = False
                )

        FROM Opportunity
        WHERE Id = '{class_id}'
            AND StageName!='Cancelled'
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
        if confirmed == True:
            conf_query = "AND StageName='Confirmed'"
        elif confirmed == "Not Cancelled":
            conf_query = "AND StageName!='Cancelled'"
        else:
            conf_query = ""
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
            SELECT Week__r.Name, Account.Name, Teacher__r.Name, Teacher__r.Phone__c, Partner_Organisation__c, Time_Schedule__r.Name
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

    def get_teacher_details(self, email):
        query = f"""
            SELECT Id, Full_Name__c, Phone__c, Email__c, Address__Street__s, Address__City__s, Address__PostalCode__s, IBAN__c, BIC__c, Birthplace__c, Nationality__c, Registration_Number__c, Contract_Type__c, Contract_Salary__c,
                Firebase_UID__c
            FROM Employee__c
            WHERE Email__c='{email}'
            """
        return query

    def get_additional_payments(self, year, month):
        query = f"""
            SELECT Beneficiary__r.Email__c, Amount__c, Name
            FROM Payment__c
            WHERE Year__c={year} AND Month__c={month}
            """
        return query
