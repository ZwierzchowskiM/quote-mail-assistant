from src.email_handler import check_emails, read_emails
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
    ask_my_assistant()


if __name__ == "__main__":
    main()

