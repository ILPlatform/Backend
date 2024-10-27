
from .SFConnector import SFConnector
from .SFQueries import SFQueries

import os
from pprint import pprint
from datetime import datetime, timedelta


class SFProcessor(SFConnector):
    def __init__(self, SF_USERNAME, SF_PASSWORD, SF_SECURITY_TOKEN, SF_DOMAIN) -> None:
        super().__init__(SF_USERNAME, SF_PASSWORD, SF_SECURITY_TOKEN, SF_DOMAIN)
        self.queries = SFQueries()

    def __process_camp_details(self, data):
        nl = '\n\n'
        address = f'{data["Account"]["BillingAddress"]["street"]}, {data["Account"]["BillingAddress"]["postalCode"]} {data["Account"]["BillingAddress"]["city"]}, {data["Account"]["BillingAddress"]["country"]}'
        processed_data = {
            "id": data["Id"],
            "code": data["Camp_Code__c"],
            "name": data["Name"],
            "event_id": data["Google_Event__c"],
            "picture_grand_parent_id": data.get("Week__r").get("Holiday__r").get("Google_Drive_Pictures_ID__c"),
            "picture_parent_id": data.get("Week__r").get("Google_Drive_Pictures_ID__c"),
            "picture_parent_name": f'{data.get("Week__r").get("Name")} ({data["Week__r"]["Start_Date__c"][8:10]}/{data["Week__r"]["Start_Date__c"][5:7]}-{data["Week__r"]["End_Date__c"][8:10]}/{data["Week__r"]["End_Date__c"][5:7]})',
            "week_name": data.get("Week__r").get("Name"),
            "week_id": data.get("Week__r").get("Id"),
            "holiday_id": data.get("Week__r").get("Holiday__r").get("Id"),
            "pictures_id": data["Google_Drive_Pictures__c"],
            "pictures_name": f'{data.get("Account").get("Name")} ({data.get("Time_Schedule__r").get("Time_Slot__c", "")[3:]})',
            "summary": f'{data["Camp_Code__c"]} - Stage {data["Account"]["Name"]} [{data["Ages_Real__c"] if data["Ages_Real__c"] != "" else "???"} ans]',
            "teacher_text": f'{data["Time_Schedule__r"]["Name"]} {data["Account"]["Name"]} ({address}) [{data["Ages_Real__c"] if data["Ages_Real__c"] != "" else "???"} ans]',
            "teacher_email": data["Teacher__r"]["Email__c"] if data["Teacher__r"] else None,
            "start_time": data["Time_Schedule__r"]["Start_Pay_Time__c"][:-1],
            "start": f'{data["Week__r"]["Start_Date__c"]}T{data["Time_Schedule__r"]["Start_Pay_Time__c"][:-1]}',
            "end_day1": f'{data["Week__r"]["Start_Date__c"]}T{data["Time_Schedule__r"]["End_Pay_Time__c"][:-1]}',
            "start_day1": f'{(data["Week__r"]["Start_Date__c"] + "T" + data.get("Time_Schedule__r", {}).get("Start_Pay_Time_Day_1__c")[:-1]) if data.get("Time_Schedule__r", {}).get("Start_Pay_Time_Day_1__c") else (data["Week__r"]["Start_Date__c"] + "T" + data["Time_Schedule__r"]["Start_Pay_Time__c"][:-1])}',
            "address": address,
            "description": f'{"".join(["Notes importantes: ", data["Description"], nl]) if data["Description"] else ""}{data["Time_Schedule__r"]["Description__c"]}',
            "excluded_day": data.get("Week__r").get("Excluded_Day__c"),
            "replacements": [{"date": replacement.get("Date__c"), "email": replacement.get("Teacher__r").get("Email__c")} for replacement in (data.get("Replacements__r") or {}).get('records', [])],
            "overwrite_cancelled": data.get("Overwrite_Cancelled__c"),
        }
        return processed_data

    def get_camp_details(self, code, confirmed=True):
        if confirmed:
            query = self.queries.get_camp_details(code)
        else:
            query = self.queries.get_possible_camp_details(code)
        data = self.sf.query(query)["records"][0]

        processed_data = self.__process_camp_details(data)

        return processed_data

    def get_all_camp_details(self, week_codes):
        query = self.queries.get_all_camp_details(week_codes)
        results = self.sf.query_all_iter(query)
        processed = [self.__process_camp_details(r) for r in results]
        return processed

    def __process_class_details(self, data):
        nl = '\n\n'
        address = f'{data["Account"]["BillingAddress"]["street"]}, {data["Account"]["BillingAddress"]["postalCode"]} {data["Account"]["BillingAddress"]["city"]}, {data["Account"]["BillingAddress"]["country"]}'


        processed_data = {
            "id": data["Id"],
            "code": data["Code__c"],
            "name": data["Name"],
            "event": {
                "id": data["Google_Event__c"],
                "school": data["Account"]["Name"],
                "summary": f'{data["Code__c"]} - {data["Account"]["Name"]} [{data["Ages_Announced__c"] if data.get("Ages_Announced__c") and data.get("Ages_Announced__c") != "" else "???"}]',
                "email": data["Teacher__r"]["Email__c"] if data["Teacher__r"] else None,
                "start_time": data["Start_Time__c"][:-1],
                "end_time": data["End_Time__c"][:-1],
                "address": address,
                "start_date": data["Yearly_Schedule__r"]["Start_Date__c"],
                "end_date": data["Yearly_Schedule__r"]["End_Date__c"],
                "day": data["Day_of_Week__c"],
                "additional_invite": data.get("Additional_Invite__c"),
                "online": data.get("Account").get("Online__c"),
            },
            "holidays": {
                "weeks": data["Yearly_Schedule__r"]["Associated_Calendar__r"]["Holiday_Weeks__c"],
                "days": data["Yearly_Schedule__r"]["Associated_Calendar__r"]["Holiday_Days__c"],
                "overwrite_cancelled_ys": data["Yearly_Schedule__r"]["Overwrite_Cancelled__c"],
                "overwrite_cancelled": data["Overwrite_Cancelled__c"],
            },
            "replacements": {
                "one_time": [{
                    "date": r.get("Date__c"),
                    "email": r["Teacher__r"].get("Email__c") if r.get("Teacher__r") else None
                } for r in filter(lambda x: x.get("RecordTypeId") == "012P5000001QASzIAO", (data.get("Replacements__r") or {}).get('records', []))],
                "permanent": [{
                    "date": r.get("Date__c"),
                    "email": r["Teacher__r"].get("Email__c") if r.get("Teacher__r") else None
                } for r in filter(lambda x: x.get("RecordTypeId") == "012P5000001QAUbIAO", (data.get("Replacements__r") or {}).get('records', []))],
            },
        }
        print(processed_data)
        return processed_data

    def get_all_class_details(self, year_code):
        query = self.queries.get_all_class_details(year_code)
        results = self.sf.query_all_iter(query)
        processed = [self.__process_class_details(r) for r in results]
        return processed

    def get_all_class_details2(self, class_details):
        query = self.queries.get_all_class_details2(class_details)
        results = self.sf.query_all_iter(query)
        results_list = list(results)
        if len(results_list) == 0:
            return None
        else:
            return self.__process_class_details(results_list[0])

    def get_all_class_details3(self, class_id):
        query = self.queries.get_all_class_details3(class_id)
        results = self.sf.query_all_iter(query)
        results_list = list(results)
        if len(results_list) == 0:
            return None
        else:
            return self.__process_class_details(results_list[0])


    def get_camp_weeks(self):
        query = self.queries.get_camp_weeks()
        data = self.sf.query_all_iter(query)

        processed_data = [{
            "code": d["Week_Code__c"],
            "period": d["Name"],
            "start": d["Start_Date__c"],
            "end": d["End_Date__c"],
            "days": d["Number_of_Days__c"]
        } for d in data]

        return processed_data

    def get_camps_per_week(self, week_code, confirmed=True):
        query = self.queries.get_camps_per_week(week_code, confirmed)
        data = self.sf.query(query)["records"]
        return [d["Camp_Code__c"] for d in data]

    def get_camps_per_week_with_name(self, week_code, confirmed=True):
        query = self.queries.get_camps_per_week(week_code, confirmed)
        data = self.sf.query(query)["records"]
        return [{"code": d["Camp_Code__c"], "name": d["Name"]} for d in data]

    def get_teachers_for_partners(self, partner, only_confirmed=True):
        query = self.queries.get_teachers_for_partners(partner, only_confirmed)
        data = self.sf.query_all_iter(query)

        processed_data = [f'{d["Week__r"]["Name"]} {d["Time_Schedule__r"]["Name"]}, {d["Account"]["Name"]} -> {d["Teacher__r"]["Name"] if d["Teacher__r"] else "???"} ({d["Teacher__r"]["Phone__c"] if d["Teacher__r"] else "???"})' for d in data]
        return processed_data

    def get_week_long_name(self, week_code):
        query = self.queries.get_week_name(week_code)
        data = self.sf.query(query)["records"][0]

        return f'{data["Name"]} ({data["Start_Date__c"]} -> {data["End_Date__c"]})'

    def get_teacher_details(self, email):
        query = self.queries.get_teacher_details(email)
        data = self.sf.query(query)["records"][0]

        nn = data.get("Registration_Number__c").replace(".", "")

        processed_data = {
            "id": data.get("Id"),
            "uid": data.get("Firebase_UID__c"),
            "name": data.get("Full_Name__c"),
            "email": data.get("Email__c"),
            "phone": data.get("Phone__c"),
            "address": f'{data.get("Address__Street__s")}, {data.get("Address__PostalCode__s")} {data.get("Address__City__s")}',
            "iban": data.get("IBAN__c"),
            "bic": data.get("BIC__c"),
            "nn": data.get("Registration_Number__c"),
            "nationality": data.get("Nationality__c"),
            "birthplace": data.get("Birthplace__c"),
            "contract_type": data.get("Contract_Type__c"),
            "contract": float(data.get("Contract_Salary__c") or 0),
            "birthdate": f"{nn[4:6]}/{nn[2:4]}/{nn[0:2]}"
        }

        return processed_data

    def create_contract(self, teacher_id, start, end, contract_type, link):
        contract = self.sf.Contract.create({
            "AccountId": os.getenv("SF_TEACHERS_ACCOUNT_ID"),
            "RecordTypeId": os.getenv("SF_TEACHER_CONTRACT_RECORD_TYPE_ID"),
            "Teacher__c": teacher_id,
            "StartDate": start,
            "Contract_End_Date__c": end,
            "Contract_Type__c": contract_type,
            "Unsigned_Contract__c": link
        })
        return list(list(contract.items())[0])[1]

    def update_contract(self, contract_id, signed_link):
        self.sf.Contract.update(contract_id, {"Signed_Contract__c": signed_link})

    def get_additional_payments(self, year, month):
        query = self.queries.get_additional_payments(year, month)
        data = self.sf.query_all_iter(query)

        processed_data = [{
            'teachers': [d.get("Beneficiary__r").get("Email__c")],
            'held': True,
            'minutes': 0,
            'amount': d["Amount__c"],
            'nice_name': f'    {d["Name"]} ({d["Amount__c"]}€)'
        } for d in data]

        return processed_data
