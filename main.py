import pandas as pd
import random
import requests
import os

# 👉 Замените на ваш токен и ID канала
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")  # Пример: -1001234567890

def get_random_prompt_from_excel(filepath):
    try:
        df = pd.read_excel(filepath, engine='openpyxl')

        # Проверяем, есть ли нужные колонки
        if "Русский" not in df.columns or "Английский" not in df.columns:
            print("Нужные колонки не найдены в Excel.")
            return None, None

        ru_prompts = df["Русский"].dropna().tolist()
        en_prompts = df["Английский"].dropna().tolist()

        if not ru_prompts or not en_prompts or len(ru_prompts) != len(en_prompts):
            print("Недостаточно данных или несовпадение строк.")
            return None, None

        idx = random.randint(0, len(ru_prompts) - 1)
        return en_prompts[idx], ru_prompts[idx]

    except Exception as e:
        print(f"Ошибка при чтении Excel: {e}")
        return None, None

def send_message_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    print(f"Ответ Telegram API: {response.status_code}, {response.text}")

def main():
    filepath = "datasets/prompts/740.xlsx"
    en_prompt, ru_prompt = get_random_prompt_from_excel(filepath)

    if not en_prompt or not ru_prompt:
        print("Не удалось получить промт.")
        return

    message = (
        "💡 *Сегодняшний промт:*\n\n"
        f"🇺🇸 *English:*\n`{en_prompt}`\n\n"
        f"🇷🇺 *Перевод:*\n`{ru_prompt}`"
    )

    send_message_telegram(message)

if __name__ == "__main__":
    main()
