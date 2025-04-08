from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import datetime
import base64


SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():

    try:
        
        load_dotenv()

        client_id = os.getenv("GOOGLE_OAUTH2_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_OAUTH2_CLIENT_SECRET")
        refresh_token = os.getenv("GOOGLE_OAUTH2_REFRESH_TOKEN")
       

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

    # Data godzinna temu w formacie Gmaila: RFC 3339
    one_hour_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    time_formatted = one_hour_ago.isoformat("T") + "Z"

    # Szukamy nieprzeczytanych maili z ostatniej godziny
    query = f'is:unread after:{int(one_hour_ago.timestamp())}'
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    for msg in messages:
        print (msg)

    matching_emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full', metadataHeaders=['Subject']).execute()
        headers = msg_data['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), '')

        if any(word in subject.lower() for word in ['oferta', 'oferty', 'ofertowe']):
            body = extract_message_body(msg_data['payload'])
            matching_emails.append({
                'id': msg['id'],
                'subject': subject,
                'body': body
            })

    return matching_emails

def extract_message_body(payload):
    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
            # Jeżeli part to tekst w formacie tekstowym, dodajemy go do body
            if part['mimeType'] == 'text/plain' and 'body' in part:
                body += decode_base64(part['body']['data'])
            # Obsługuje przypadek, gdy są inne części, np. HTML
            elif part['mimeType'] == 'text/html' and 'body' in part:
                body += decode_base64(part['body']['data'])
    return body if body else "Brak treści wiadomości"

def decode_base64(data):
    return base64.urlsafe_b64decode(data).decode('utf-8')

def read_emails(emails):
    for email in emails:
        print(f"Temat: {email['subject']}")
        print(f"Treść:\n{email['body']}\n")
        # Tutaj możesz dodać wysyłanie do OpenAI
