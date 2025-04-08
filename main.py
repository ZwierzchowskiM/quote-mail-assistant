from src.email_handler import check_emails, send_email
from src.openai_client import ask_chatgpt, ask_my_assistant

#def job():
   

#def check_app_status():

 #   response = requests.get("https://news-title-bot.onrender.com/ping")
 #   if response.status_code == 200:
 #       print("App status: OK")
 #   else:
 #       print(f"Unexpected status code: {response.status_code}")



def main():
    
    print("App start")
    emails_with_quote = check_emails()
    # read_emails(emails_with_quote)

    for email in emails_with_quote:
        assistant_response = ask_my_assistant()
        response_text = assistant_response["response"]
        attach_offer_pdf = assistant_response["attach_offer_pdf"]

        # Konfiguracja maila – zmień wg własnych potrzeb
        recipient = email['from']
        subject = "Odpowiedź na zapytanie ofertowe"
        body = response_text

        # Jeżeli asystent wskazał, że dołączyć ofertę, ustaw ścieżkę do pliku (później pobierzemy właściwy plik z Google Drive)
        if attach_offer_pdf:
            #pobrania danych z gmaila
            attachement = None 
        else:
            attachement = None
        # Wysyłamy maila
        send_email(recipient, subject, body, attachement)


if __name__ == "__main__":
    main()

