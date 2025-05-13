import os
import random
import pandas as pd
import telegram

# Константы
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
EXCEL_PATH = "datasets/prompts/740.xlsx"

def load_prompt_from_excel(file_path):
    try:
        df = pd.read_excel(file_path, header=1)  # Заголовки на второй строке
        if 'Английский' not in df.columns or 'Русский' not in df.columns:
            print("Нужные колонки не найдены в Excel.")
            return None
        row = df.sample(1).iloc[0]
        return row['Английский'], row['Русский']
    except Exception as e:
        print(f"Ошибка при загрузке Excel: {e}")
        return None

def main():
    bot = telegram.Bot(token=BOT_TOKEN)

    prompt = load_prompt_from_excel(EXCEL_PATH)
    if prompt is None:
        print("Не удалось получить промт.")
        return

    english_prompt, russian_prompt = prompt

    message = (
        "💡 *Сегодняшний промт:*\n\n"
        f"*EN:*\n```\n{english_prompt}\n```\n\n"
        f"*RU:*\n```\n{russian_prompt}\n```"
    )

    bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')

if __name__ == "__main__":
    main()
