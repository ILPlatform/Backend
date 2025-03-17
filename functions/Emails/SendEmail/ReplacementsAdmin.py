from Emails import send_email_admin

def sendEmail_ReplacementsAdmin(details):
    # Send email to admins
    send_email_admin(
        subject=f"""{details.get('RecordType').get('Name')} Replacement {details.get('Opportunity__r').get('Code__c')}:
            {details.get('Teacher_Old__r', {}).get('Full_Name__c')} ->
            {details.get('Teacher__r', {}).get('Full_Name__c')}""",
        body=f"""
            <p>Dear Admins,</p>
            <p>A replacement has been recorded for the class <b>{details.get('Opportunity__r').get('Code__c')}</b>
                on <b>{details.get('Date__c')}</b>.</p>
            <p>Here are the details regarding the replacement:</p>
            <ul>
                <li><b>Code:</b> {details.get("Opportunity__r").get("Code__c")}</li>
                <li><b>Day:</b> {details.get('Opportunity__r').get("Day_of_Week__c")}</li>
                <li><b>Time Slot:</b> {details.get('Opportunity__r').get("Start_Time__c")}
                    - {details.get('Opportunity__r').get("End_Time__c")}</li>
                <li><b>Replacement Date:</b> {details.get('Date__c')}</li>
                <li><b>Replacement Type:</b> {details.get('RecordType').get('Name')}</li>
                <li><b>Old Teacher:</b> {details.get('Teacher_Old__r', {}).get('Full_Name__c')}</li>
                <li><b>New Teacher:</b> {details.get('Teacher__r', {}).get('Full_Name__c')}</li>
                <li><b>Reason:</b> {details.get('Reason__c')}</li>
            </ul>
            <p>Kind regards, <br></p>
        """
    )
