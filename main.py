from src.email_handler import check_emails, send_email
from src.openai_client import ask_chatgpt, ask_my_assistant
from src.google_drive_handler import download_file_from_drive
import os
import requests
import threading
import schedule
import time
from src.app import app 


def start_flask():
    app.run(host='0.0.0.0', port=8000)

def job():
    emails_with_quote = check_emails()
    

    for email in emails_with_quote:
        assistant_response = ask_my_assistant()
        response_text = assistant_response["response"]
        attach_offer_pdf = assistant_response["attach_offer_pdf"]

        
        recipient = email['from']
        subject = "Odpowiedź na zapytanie ofertowe"
        body = response_text

        if attach_offer_pdf:
            file_id = os.getenv("GOOGLE_DRIVE_OFFER_FILE_ID")
            attachement = download_file_from_drive(file_id)
        else:
            attachement = None
        send_email(recipient, subject, body, attachement)

def check_app_status():

    response = requests.get("https://quote-mail-assistant.onrender.com/ping")
    if response.status_code == 200:
        print("App status: OK")
    else:
        print(f"Unexpected status code: {response.status_code}")


def main():
    
    print("App start")
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()


    schedule.every().day.at("10:30").do(job)
    schedule.every(2).minutes.do(check_app_status)
    
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()

