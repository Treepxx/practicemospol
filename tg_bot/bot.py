import asyncio
import sqlite3
import logging
import os                           
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

load_dotenv() 
TOKEN = os.getenv("TOKEN") 
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

def init_db():
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            review_text TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        "Привет! 👋\n"
        "Я бот для сбора отзывов о нашем проекте. "
        "Напиши сюда всё, что думаешь о продукте!"
    )
    await message.answer(welcome_text)

@dp.message(F.text)
async def handle_review(message: types.Message):
    review = message.text
    username = message.from_user.username or message.from_user.first_name

    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reviews (username, review_text) VALUES (?, ?)', (username, review))
    conn.commit()
    conn.close()

    await message.answer("Спасибо за отзыв! Твое мнение очень важно для нас!🤝")

async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())