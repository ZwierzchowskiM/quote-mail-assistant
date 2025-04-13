from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import io
import os
from io import BytesIO
from dotenv import load_dotenv

def download_file_from_drive(file_id):
    
    creds = authenticate_gmail()
    drive_service = build('drive', 'v3', credentials=creds)

    try:
        request = drive_service.files().get_media(fileId=file_id)
        
        file_metadata = drive_service.files().get(fileId=file_id, fields='name').execute()
        file_name = file_metadata['name']

      
        request = drive_service.files().get_media(fileId=file_id)
        file_data = BytesIO(request.execute())

        file_data.name = file_name

        print(f"Pobrano plik: {file_name}")
        return file_data

    except Exception as e:
        print(f"Błąd podczas pobierania pliku z Google Drive: {e}")
        return None
    


def authenticate_gmail():

    try:
        
        #load_dotenv()

        client_id = os.getenv("GOOGLE_OAUTH2_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_OAUTH2_CLIENT_SECRET")
        refresh_token = os.getenv("GOOGLE_OAUTH2_REFRESH_TOKEN")
       

        if not client_id or not client_secret or not refresh_token:
            raise ValueError("Brak wymaganych danych do uwierzytelnienia Drive API.")

        creds = Credentials.from_authorized_user_info(
            info={
                'client_id': client_id,
                'client_secret': client_secret,
                'refresh_token': refresh_token,
                'token': '', 
            },
        )

        if creds.expired or not creds.valid:
            creds.refresh(Request())

        return creds
    
    except Exception as e:
        print(f"Błąd uwierzytelnienia Drive API: {e}")
        return None 
