from dotenv import load_dotenv
import time
import os
from openai import OpenAI
import json


load_dotenv()

def get_openai_client():
    return OpenAI()

def ask_chatgpt():
    
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Jesteś asystentem handlowym firmy sprzedającej marmury."},
            {"role": "user", "content": "Opowiedz o twojej firmie"}
        ]
    )
    print (response.choices[0].message.content)


def ask_my_assistant(thread_id=None, message="Szukam marmuru na blaty kuchenne. Jakie macie beżowe marmury?"):
    client = get_openai_client()
    assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

   
    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id

    
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )

    
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run.status == "completed":
            break
        elif run.status == "failed":
            raise Exception("Run failed.")
        time.sleep(1) 

   
    messages = client.beta.threads.messages.list(thread_id=thread_id)

    
    response_json_str = messages.data[0].content[0].text.value  
    print("\nWPełny tekst odpowiedzi:")
    print(response_json_str)  

    try:
        response_json = json.loads(response_json_str)  
    except json.JSONDecodeError:
        print("Błąd parsowania JSON!")
        return None

    
    response = response_json.get("response", "")  
    attach_offer_pdf = response_json.get("attach_offer_pdf", False)  

    

    print("\nWydzielony tekst odpowiedzi:")
    print(response)  

    print("\nInformacja o załączniku:")
    print("Tak" if attach_offer_pdf else "Nie")  
    
    return {
        "response": response,
        "attach_offer_pdf": attach_offer_pdf
    }