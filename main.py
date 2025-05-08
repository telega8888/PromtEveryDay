import csv
import random
import os
from telegram import Bot
from telegram.ext import Application, ContextTypes
from telegram.ext import JobQueue
import datetime

# Получаем токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@название_твоего_канала"  # Пример: "@prompt_every_day"

# Загружаем промты из CSV
def load_prompts():
    with open("prompts.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return [f"🧠 *{row['act']}*\n\n{row['prompt']}" for row in reader]

prompts = load_prompts()

# Задача: отправить случайный промт в канал
async def send_prompt(context: ContextTypes.DEFAULT_TYPE):
    prompt = random.choice(prompts)
    await context.bot.send_message(chat_id=CHANNEL_ID, text=prompt, parse_mode="Markdown")

# Основной запуск
async def main():
    application = Application.builder().token(TOKEN).build()
    job_queue = application.job_queue

    # Отправка каждый день в 10:00 UTC
    job_queue.run_daily(send_prompt, time=datetime.time(hour=10, minute=0))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
