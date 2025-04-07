from src.email_handler import check_emails

#def job():
   

#def check_app_status():

 #   response = requests.get("https://news-title-bot.onrender.com/ping")
 #   if response.status_code == 200:
 #       print("App status: OK")
 #   else:
 #       print(f"Unexpected status code: {response.status_code}")



def main():
    
    print("App start")
    check_emails()

if __name__ == "__main__":
    main()

