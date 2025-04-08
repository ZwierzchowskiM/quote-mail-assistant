from dotenv import load_dotenv
import time
import os
from openai import OpenAI


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


def ask_my_assistant(thread_id=None, message="Jakie macie płyty marmurowe?"):
    client = get_openai_client()
    assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

    # Tworzymy nowy wątek jeśli nie został podany
    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id

    # Dodajemy wiadomość użytkownika do wątku
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )

    # Uruchamiamy "run" – czyli zapytanie asystenta
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    # Czekamy aż run się zakończy (status == "completed")
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run.status == "completed":
            break
        elif run.status == "failed":
            raise Exception("Run failed.")
        time.sleep(1)  # Poczekaj chwilę przed kolejnym sprawdzeniem

    # Pobieramy odpowiedź
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    response = messages.data[0].content[0].text.value

    print("Odpowiedź asystenta:\n", response)
    return response