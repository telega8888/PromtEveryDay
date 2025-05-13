import os
import pandas as pd
import random
import telegram

# Настройки
EXCEL_PATH = "datasets/prompts/740.xlsx"
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Инициализация бота
bot = telegram.Bot(token=BOT_TOKEN)

def get_random_prompt(path):
    try:
        # Заголовки находятся во 2-й строке → header=1
        df = pd.read_excel(path, header=1)
        if 'Русский' not in df.columns or 'Английский' not in df.columns:
            print("Нужные колонки не найдены в Excel.")
            return None, None

        row = df.sample().iloc[0]
        return row['Русский'], row['Английский']
    except Exception as e:
        print(f"Ошибка при чтении Excel: {e}")
        return None, None

def format_message(russian, english):
    return f"💡 *Промт дня*\n\n🇷🇺 *Русский*\n{russian}\n\n🇬🇧 *English*\n{english}"

def main():
    ru, en = get_random_prompt(EXCEL_PATH)
    if not ru or not en:
        print("Не удалось получить промт.")
        return

    message = format_message(ru, en)
    bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode=telegram.constants.ParseMode.MARKDOWN)

if __name__ == "__main__":
    main()
