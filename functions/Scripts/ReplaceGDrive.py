from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io
from firebase_admin import storage

def replace_gdrive_firebase(google, sf, id):
    print(f"Lauching replace_gdrive_firebase for {id}")

    # Get the image_url from SF
    result = sf.sf.query(f"SELECT Image_URL__c FROM Employee__c WHERE Id='{id}'").get("records", [{}])[0].get("Image_URL__c", None)

    # Check if the image_url is from Google Drive
    if not result or "drive.google.com" not in result:
        return

    # Get the image_id from the image_url
    image_id = result.split("id=")[-1]

    # Download the image from Google Drive
    request = google.drive.files().get_media(fileId=image_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)
    image_data = fh.read()

    # Upload the image to Firebase
    blob = storage.bucket().blob("Images/" + id + ".jpg")
    blob.upload_from_string(image_data, content_type='image/jpeg')
    print(f"Image uploaded")

    # Make the blob publicly accessible
    blob.make_public()

    # Get the public URL
    url = blob.public_url

    # Update the image_url in SF
    sf.sf.Employee__c.update(id, {"Image_URL__c": url})
