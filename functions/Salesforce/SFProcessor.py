
from .SFConnector import SFConnector
from .SFQueries import SFQueries

import os

class SFProcessor(SFConnector):
    def __init__(self, SF_USERNAME, SF_PASSWORD, SF_SECURITY_TOKEN) -> None:
        super().__init__(SF_USERNAME, SF_PASSWORD, SF_SECURITY_TOKEN)
        self.queries = SFQueries()

    def get_camp_details(self, code, confirmed=True):
        if confirmed:
            query = self.queries.get_camp_details(code)
        else:
            query = self.queries.get_possible_camp_details(code)
        data = self.sf.query(query)["records"][0]

        nl = '\n\n'
        address = f'{data["Account"]["BillingAddress"]["street"]}, {data["Account"]["BillingAddress"]["postalCode"]} {data["Account"]["BillingAddress"]["city"]}, {data["Account"]["BillingAddress"]["country"]}'
        processed_data = {
            "id": data["Id"],
            "code": code,
            "event_id": data["Google_Event__c"],
            "summary": f'{code} - Stage {data["Account"]["Name"]} [{data["Ages_Real__c"] if data["Ages_Real__c"] != "" else "???"} ans]',
            "teacher_text": f'{data["Time_Schedule__r"]["Name"]} {data["Account"]["Name"]} ({address}) [{data["Ages_Real__c"] if data["Ages_Real__c"] != "" else "???"} ans]',
            "teacher_email": data["Teacher__r"]["Email"] if data["Teacher__r"] else None,
            "start": f'{data["Week__r"]["Start_Date__c"]}T{data["Time_Schedule__r"]["Start_Pay_Time__c"][:-1]}',
            "end_day1": f'{data["Week__r"]["Start_Date__c"]}T{data["Time_Schedule__r"]["End_Pay_Time__c"][:-1]}',
            "address": address,
            "description": f'{"".join(["Notes importantes: ", data["Description"], nl]) if data["Description"] else ""}{data["Time_Schedule__r"]["Description__c"]}'
        }

        return processed_data

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

        processed_data = [f'{d["Week__r"]["Name"]} {d["Time_Schedule__r"]["Name"]}, {d["Account"]["Name"]} -> {d["Teacher__r"]["Name"] if d["Teacher__r"] else "???"} ({d["Teacher__r"]["Phone"] if d["Teacher__r"] else "???"})' for d in data]
        return processed_data

    def get_week_long_name(self, week_code):
        query = self.queries.get_week_name(week_code)
        data = self.sf.query(query)["records"][0]

        return f'{data["Name"]} ({data["Start_Date__c"]} -> {data["End_Date__c"]})'

    def get_teacher_details(self, email):
        query = self.queries.get_teacher_details(email)
        data = self.sf.query(query)["records"][0]

        nn = data.get("National_Registration_Number__c").replace(".", "")

        processed_data = {
            "id": data.get("Id"),
            "name": data.get("Name"),
            "email": data.get("Email"),
            "phone": data.get("Phone"),
            "address": f'{data.get("MailingStreet")}, {data.get("MailingPostalCode")} {data.get("MailingCity")}',
            "iban": data.get("IBAN__c"),
            "bic": data.get("BIC_Code__c"),
            "nn": data.get("National_Registration_Number__c"),
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
