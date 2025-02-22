from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=10)
def payments_a_get_processed(data):
    # Initialize DB and SF
    sf = getSF()

    # Get all payments from SF
    sf_results = list(sf.sf.query_all_iter(f"""
        SELECT
            Id, Amount__c, Year__c, Month__c, Paid__c,
            Beneficiary__r.Id, Beneficiary__r.Full_Name__c,
            Document__r.Id, CreatedDate,
            Contract__c, Updated__c, Type_of_Payment__c
        FROM Payment__c
        WHERE RecordTypeId = '012P5000001tRevIAE' and Deleted__c = False
    """))

    # Get all documents from SF
    sf_docs = list(sf.sf.query_all_iter(f"""
        SELECT
            Id, Signed__c
        FROM Document__c
        WHERE RecordTypeId = '012P5000001T8MbIAK'
    """))

    # Process data
    users = set(list(map(lambda x: x.get('Beneficiary__r', {}).get('Id'), sf_results)))
    get_name = lambda user: list(filter(lambda x: x.get('Beneficiary__r', {}).get('Id') == user, sf_results))[0].get('Beneficiary__r').get('Full_Name__c')
    results = {
        user: {
            "id": user,
            "name": get_name(user),
            "pays": []
        }
        for user in users
    }

    # Process documents
    docs = {
        doc.get('Id'): {
            "id": doc.get('Id'),
            "signed": doc.get('Signed__c')
        }
        for doc in sf_docs
    }

    is_manager = lambda x: x.get('Type_of_Payment__c') == "Manager Salary"
    is_contract = lambda x: x.get('Type_of_Payment__c') == "Student Contract"
    is_signed = lambda x: docs.get(x.get('Document__r').get('Id')).get('signed') if x.get('Document__r') else False
    is_signed2 = lambda x: is_signed(x) or is_manager(x)
    is_updated = lambda x: x.get('Updated__c')

    # Combine documents and payments
    for payment in sorted(sf_results, key=lambda x: x.get('CreatedDate'), reverse=True):
        results[payment.get('Beneficiary__r').get('Id')]["pays"].append({
            "payment_id": payment.get('Id'),
            "month": payment.get('Month__c'),
            "year": payment.get('Year__c'),
            "amount": payment.get('Amount__c'),
            "to_pay":
                not payment.get('Paid__c')
                    and is_signed2(payment)
                    and not (is_contract(payment) and not is_updated(payment)),
            "to_update": is_signed(payment) and is_contract(payment) and not is_updated(payment),
            "paid": payment.get('Paid__c'),
            "contract_type": payment.get('Type_of_Payment__c'),
        })


    return {"data": {"response": list(results.values()), "status": 200}}
