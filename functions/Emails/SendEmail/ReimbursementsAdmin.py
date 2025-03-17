from Emails import send_email_admin

def sendEmail_ReimbursementsAdmin(details):
    # Send email to admins
    send_email_admin(
        subject="""New reimbursement request""",
        body=f"""
            <p>Dear Admins,</p>
            <p>A reimbursement claim has been recorded by {details.get("Employee__r", {}).get("Full_Name__c")}.</p>
            <p>Here are the details regarding the reimbursement:</p>
            <ul>
                <li><b>Date:</b> {details.get('Date__c')}</li>
                <li><b>Amount:</b> {details.get('Amount__c')}</li>
                <li><b>Summary:</b> {details.get('Summary__c')}</li>
                <li><b>Justification:</b> {details.get('Justification__c')}</li>
            </ul>
            <p>Kind regards, <br></p>
        """
    )
