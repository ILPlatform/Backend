import os
from pprint import pprint

SHEETS_PAYMENTS_ID = os.getenv('SHEETS_PAYMENTS_ID')

def update_payment_sheet(google, teacher_dict, year, month):
    search_range = f'{year}!A1:O200'
    result = google.sheets.spreadsheets().values().get(
        spreadsheetId=SHEETS_PAYMENTS_ID,
        range=search_range
    ).execute()
    payment_sheets = result.get('values', [])

    for teacher_email in teacher_dict:
        teacher = teacher_dict.get(teacher_email)
        for i, line in enumerate(payment_sheets):
            if line[0].replace(" ", "").lower() == teacher.get('name').replace(" ", "").lower():
                if payment_sheets[i][month] == '':
                    payment_sheets[i][month] = teacher.get('total_amount')
                else:
                    if len(teacher_dict.keys()) == 1:
                        print(f"[WARNING] Payment sheet already filled out for {teacher.get('name')} with value {payment_sheets[i][month]}")
                        print(f"[WARNING] Overwriting value, only possible since single attestation!")
                        payment_sheets[i][month] = teacher.get('total_amount')
                    else:
                        raise ValueError(f"[ERROR] Payment sheet already filled out for {teacher.get('name')} with value {payment_sheets[i][month]}")
                break
        else:
            raise ValueError(f"[ERRROR] Teacher {teacher.get('name')} not present in payment sheet!! Please add him/her and re-try")

    # Write the updated data back to the spreadsheet
    update_range = f"{year}!{chr(ord('A') + month)}1:{chr(ord('A') + month)}{len(payment_sheets)}"
    update_body = {
        'values': list(map(lambda x: [x[month]], payment_sheets))
    }
    update_result = google.sheets.spreadsheets().values().update(
        spreadsheetId=SHEETS_PAYMENTS_ID,
        range=update_range,
        valueInputOption='USER_ENTERED',
        body=update_body
    ).execute()
