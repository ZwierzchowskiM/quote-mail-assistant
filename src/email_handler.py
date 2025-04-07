from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Zakresy uprawnień do Gmaila
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():

    try:
        
        load_dotenv()

        client_id = os.getenv("GOOGLE_OAUTH2_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_OAUTH2_CLIENT_SECRET")
        refresh_token = os.getenv("GOOGLE_OAUTH2_REFRESH_TOKEN")
        print(client_id )

        if not client_id or not client_secret or not refresh_token:
            raise ValueError("Brak wymaganych danych do uwierzytelnienia Gmail API.")

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
        print(f"Błąd uwierzytelnienia Gmail API: {e}")
        return None 

def check_emails():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
    messages = results.get('messages', [])
    for msg in messages:
        message = service.users().messages().get(userId='me', id=msg['id']).execute()
        snippet = message['snippet']
        print(f"Nowa wiadomość: {snippet}")
        # Tutaj możesz dodać logikę do rozpoznawania zapytania
