import csv 
import random
import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

PROMPT_FILES = [
    "prompts.csv",
    "datasets/prompts/GPTFuzzer.csv"
]

TRANSLATED_FILE = "translated_prompts.csv"

def get_all_prompts():
    prompts = []
    for file in PROMPT_FILES:
        if not os.path.exists(file):
            continue
        with open(file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                prompt = row.get("prompt") or row.get("Prompt") or row.get("text")
                if prompt and "http" not in prompt:
                    prompts.append(prompt.strip())
    return prompts

def load_translations():
    translations = {}
    if os.path.exists(TRANSLATED_FILE):
        with open(TRANSLATED_FILE, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    en, ru = row
                    translations[en.strip()] = ru.strip()
    return translations

def save_translation(original, translated):
    with open(TRANSLATED_FILE, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([original.strip(), translated.strip()])

def translate_to_russian(text):
    print(f"Перевод: {text[:60]}...")  # Выводим первые 60 символов для отслеживания
    try:
        response = requests.post(
            "https://lt.psf.lt/translate",
            data={
                "q": text,
                "source": "en",
                "target": "ru",
                "format": "text"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(f"Ответ от переводчика: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            return result.get("translatedText", text)  # если не нашли переведённый текст — возвращаем оригинал
        else:
            print(f"Ошибка API перевода: {response.status_code}")
            return text
    except Exception as e:
        print(f"Ошибка при запросе к API перевода: {e}")
        return text  # возвращаем оригинал при ошибке

def send_to_telegram(text):
    message = f"💡 Сегодняшний промт:\n\n{text}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    print(f"Ответ Telegram API: {response.status_code}, {response.text}")

if __name__ == "__main__":
    all_prompts = get_all_prompts()
    if not all_prompts:
        send_to_telegram("Промты не найдены.")
    else:
        chosen_prompt = random.choice(all_prompts)
        translations = load_translations()

        if chosen_prompt in translations:
            translated = translations[chosen_prompt]
        else:
            translated = translate_to_russian(chosen_prompt)
            save_translation(chosen_prompt, translated)

        send_to_telegram(translated)
