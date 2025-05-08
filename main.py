import csv
import random
import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # формат: @your_channel

def get_random_prompt(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        prompts = [row["prompt"] for row in reader if "prompt" in row]
        return random.choice(prompts)

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text
    }
    response = requests.post(url, data=payload)
    print(response.status_code, response.text)

if __name__ == "__main__":
    prompt = get_random_prompt("prompts.csv")
    send_to_telegram(prompt)
