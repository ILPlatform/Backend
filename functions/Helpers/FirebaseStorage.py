from firebase_admin import storage
from datetime import datetime, timezone

class Storage:
    def __init__(self):
        self.bucket = storage.bucket("ilplatform.appspot.com")

    # Function to get a certain image url
    def get_image_url(self, path):
        blob = self.bucket.blob(path)
        current_time = int(datetime.now(tz=timezone.utc).timestamp())
        url = blob.generate_signed_url(current_time + 3600)  # URL expires in 1 hour
        return url
