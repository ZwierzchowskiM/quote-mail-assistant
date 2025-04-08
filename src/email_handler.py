from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

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

   
    one_hour_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    time_formatted = one_hour_ago.isoformat("T") + "Z"

   
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
        sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), '')  
        if any(word in subject.lower() for word in ['oferta', 'oferty', 'ofertowe']):
            body = extract_message_body(msg_data['payload'])
            matching_emails.append({
                'id': msg['id'],
                'subject': subject,
                'from': sender,         
                'body': body
        })


    return matching_emails

def extract_message_body(payload):
    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
           
            if part['mimeType'] == 'text/plain' and 'body' in part:
                body += decode_base64(part['body']['data'])
            elif part['mimeType'] == 'text/html' and 'body' in part:
                body += decode_base64(part['body']['data'])
    return body if body else "Brak treści wiadomości"

def decode_base64(data):
    return base64.urlsafe_b64decode(data).decode('utf-8')

def read_emails(emails):
    for email in emails:
        print(f"Temat: {email['subject']}")
        print(f"Treść:\n{email['body']}\n")


#---------------------------------------------------------------------

def create_mime_message(to, subject, body_text, attachment_file=None, attachment_name=None):
    
    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject
    text_part = MIMEText(body_text, 'plain')
    message.attach(text_part)

    if attachment_file is not None:
        try:
           
            if hasattr(attachment_file, 'read'):
                attachment_data = attachment_file.read()
                
                if attachment_name is None:
                    attachment_name = getattr(attachment_file, 'name', 'attachment.pdf')
            else:
                raise TypeError("attachment_file musi być ścieżką, obiektem pliku lub danymi binarnymi")
                
            part = MIMEBase('application', 'pdf')
            part.set_payload(attachment_data)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=attachment_name)
            message.attach(part)
            
        except Exception as e:
            print(f"Wystąpił błąd podczas dodawania załącznika: {e}. Wiadomość zostanie wysłana bez załącznika.")
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}


def send_email(to, subject, body_text, attachment_path=None):
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)


    mime_message = create_mime_message(to, subject, body_text, attachment_path)

    try:
        sent_message = service.users().messages().send(userId='me', body=mime_message).execute()
        print("Wiadomość wysłana. ID:", sent_message['id'])
    except Exception as e:
        print("Błąd podczas wysyłania maila:", e)