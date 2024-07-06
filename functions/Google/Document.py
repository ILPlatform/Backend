from google.oauth2 import service_account
from datetime import datetime
import os
from datetime import date

ATTESTATION_TEMPLATE_ID = os.getenv('ATTESTATION_TEMPLATE_ID')
PRESTATION_TEMPLATE_ID = os.getenv('PRESTATION_TEMPLATE_ID')
CONVENTION_TEMPLATE_ID = os.getenv('CONVENTION_TEMPLATE_ID')
DOCUMENTS_BY_BOT_ID = os.getenv('DOCUMENTS_BY_BOT_ID')
PAYMENTS_TEMPLATE_ID = os.getenv('PAYMENTS_TEMPLATE_ID')

class Document():
    def __init__(self, google):
        self.google = google

        self.log_details = None
        self.document_id = None

    def __copy_document(self, file_id, name, log_details):
        # Copy the document
        copy_request_body = {'name': name, 'parents': [DOCUMENTS_BY_BOT_ID]}
        document = self.google.drive.files().copy(fileId=file_id, body=copy_request_body).execute()

        # Log success status
        if 'id' not in document:
            print(f"[ERROR] {log_details} - Error in copying file")
            return None
        print(f"[SUCCESS] {log_details} - Copied Timesheet Document Successfully")

        return document['id']

    def get_download_link(self):
        try:
            # Create permission
            self.google.drive.permissions().create(
                fileId=self.document_id,
                body={'role': 'commenter', 'type': 'anyone'}
            ).execute()

            # Get the web view link
            file = self.google.drive.files().get(fileId=self.document_id, fields='webViewLink').execute()
            web_view_link = file.get('webViewLink', '')

            # Construct the download link
            download_link = f"{web_view_link.split('edit')[0]}export?format=pdf"
            print(f"[SUCCESS] {self.log_details} - Download Link Generated Successfully: {download_link}")

            return download_link

        except Exception as e:
            print(f"[ERROR] {self.log_details} - Error Occurred: {e}")
            return None

class TimesheetDocument(Document):
    def __init__(self, google, teacher, year, month):
        Document.__init__(self, google)
        self.teacher = teacher
        self.year = year
        self.month = month

        file_id = PRESTATION_TEMPLATE_ID if teacher.get('contract') else ATTESTATION_TEMPLATE_ID
        name = f"{year}-{month} {'Prestations' if teacher.get('contract') else 'Attestation'} {teacher.get('name')}"
        log_details = teacher.get('name')
        self.log_details = log_details
        self.document_id = self._Document__copy_document(file_id, name, log_details)

    def fill(self):
        try:
            # Create requests to replace text
            month_names_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
            requests = [
                {'replaceAllText': {'containsText': {'text': '{YEAR}'}, 'replaceText': str(self.year)}},
                {'replaceAllText': {'containsText': {'text': '{MONTH_FR}'}, 'replaceText': month_names_fr[self.month - 1]}},
                {'replaceAllText': {'containsText': {'text': '{NAME}'}, 'replaceText': self.teacher.get('name')}},
                {'replaceAllText': {'containsText': {'text': '{REGISTER_NUMBER}'}, 'replaceText': self.teacher.get('nn')}},
                {'replaceAllText': {'containsText': {'text': '{ADDRESS}'}, 'replaceText': self.teacher.get('address')}},
                {'replaceAllText': {'containsText': {'text': '{TOTAL_HOURS}'}, 'replaceText': f"{self.teacher.get('hours')}h{self.teacher.get('minutes')}"}},
                {'replaceAllText': {'containsText': {'text': '{TOTAL_AMOUNT}'}, 'replaceText': str(self.teacher.get('total_amount'))}},
                {'replaceAllText': {'containsText': {'text': '{DESCRIPTIONS_FR}'}, 'replaceText': '\n'.join(list(map(lambda x: x.get('nice_name'), self.teacher.get('events'))))}},
                {'replaceAllText': {'containsText': {'text': '{TOTAL_HOURS_SECOND_HOURS}'}, 'replaceText': str(round(self.teacher.get('total_amount') / self.teacher.get('contract'))) if self.teacher.get('contract') > 0 else "0"}},
                {'replaceAllText': {'containsText': {'text': '{TOTAL_HOURS_SECOND_MIN}'}, 'replaceText': str(round(((self.teacher.get('total_amount') / self.teacher.get('contract')) % 1) * 60)) if self.teacher.get('contract') > 0 else "0"}},
                {'replaceAllText': {'containsText': {'text': '{SALARY}'}, 'replaceText': str(self.teacher.get('contract'))}}
            ]

            # Send the batchUpdate request
            self.google.docs.documents().batchUpdate(documentId=self.document_id, body={'requests': requests}).execute()
            print(f"[SUCCESS] {self.teacher.get('name')} - Document Filled Out Successfully")

        except Exception as e:
            raise IndexError(f"[ERROR] {self.teacher.get('name')} - Error In Filling Out File: {e}")


class ConventionDocument(Document):
    def __init__(self, google, teacher):
        Document.__init__(self, google)
        self.teacher = teacher

        file_id = CONVENTION_TEMPLATE_ID
        name = f"Convention ILPlatform {teacher.get('name')}"
        log_details = teacher.get('name')
        self.log_details = log_details
        self.document_id = self._Document__copy_document(file_id, name, log_details)

    def fill(self):
        try:
            # Create requests to replace text
            requests = [
                {'replaceAllText': {'containsText': {'text': '{NAME}'}, 'replaceText': self.teacher.get('name')}},
                {'replaceAllText': {'containsText': {'text': '{REG_NUMBER}'}, 'replaceText': self.teacher.get('nn')}},
                {'replaceAllText': {'containsText': {'text': '{ADDRESS}'}, 'replaceText': self.teacher.get('address')}},
                {'replaceAllText': {'containsText': {'text': '{TODAY}'}, 'replaceText': str(date.today())}},
                {'replaceAllText': {'containsText': {'text': '{END_DATE}'}, 'replaceText': "2024-08-31"}},
                {'replaceAllText': {'containsText': {'text': '{IBAN}'}, 'replaceText': self.teacher.get('iban')}},
                {'replaceAllText': {'containsText': {'text': '{BIC}'}, 'replaceText': self.teacher.get('bic')}},
            ]

            # Send the batchUpdate request
            self.google.docs.documents().batchUpdate(documentId=self.document_id, body={'requests': requests}).execute()
            print(f"[SUCCESS] {self.teacher.get('name')} - Document Filled Out Successfully")

        except Exception as e:
            raise ValueError(f"[ERROR] {self.teacher.get('name')} - Error In Filling Out File: {e}")

class PaymentsDocument(Document):
    def __init__(self, google, total_text, payments_text, month, year):
        Document.__init__(self, google)
        self.payments_text = payments_text
        self.total_text = total_text
        self.month = month
        self.year = year

        file_id = PAYMENTS_TEMPLATE_ID
        name = f"{year}-{month} Relevés de Paiements"
        log_details = f"Relevés {year}-{month}"
        self.log_details = log_details
        self.document_id = self._Document__copy_document(file_id, name, log_details)

    def fill(self):
        try:
            # Get full month name
            month_names = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
            month_shift = self.month - 1
            month = month_names[month_shift]

            # Create requests to replace text
            requests = [
                {'replaceAllText': {'containsText': {'text': '{MONTH}'}, 'replaceText': str(month)}},
                {'replaceAllText': {'containsText': {'text': '{YEAR}'}, 'replaceText': str(self.year)}},
                {'replaceAllText': {'containsText': {'text': '{TODAY}'}, 'replaceText': str(date.today())}},
                {'replaceAllText': {'containsText': {'text': '{DETAILS_TOT}'}, 'replaceText': self.total_text}},
                {'replaceAllText': {'containsText': {'text': '{DETAILS}'}, 'replaceText': self.payments_text}}
            ]

            # Send the batchUpdate request
            self.google.docs.documents().batchUpdate(documentId=self.document_id, body={'requests': requests}).execute()
            print(f"[SUCCESS] {self.log_details} - Document Filled Out Successfully")

        except Exception as e:
            print(f"[ERROR] {self.log_details} - Error In Filling Out File: {e}")
            return None
