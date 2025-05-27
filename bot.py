
import asyncio
import logging
import os
import json
import random
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web

API_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Загрузка сказок
with open("data/fairy_tales.json", encoding="utf-8") as f:
    fairy_tales = json.load(f)

# Загрузка изображений котиков
with open("data/cat_gallery.json", encoding="utf-8") as f:
    cat_gallery = json.load(f)

# Меню
menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Хочу милого котёнка! 🐾", callback_data="cat")],
    [InlineKeyboardButton(text="Статистика 📊", callback_data="stats")],
    [InlineKeyboardButton(text="Кошачьи сказки 🌙", callback_data="fairy")],
    [InlineKeyboardButton(text="Галерея уюта 🏠", callback_data="gallery")],
])

# Хранилище статистики
user_data_path = "data/user_data.json"
if os.path.exists(user_data_path):
    with open(user_data_path, encoding="utf-8") as f:
        user_data = json.load(f)
else:
    user_data = {}

def save_user_data():
    with open(user_data_path, "w", encoding="utf-8") as f:
        json.dump(user_data, f, indent=2, ensure_ascii=False)

def get_rank(count):
    if count < 10:
        return "Маленький котёнок ⭐"
    elif count < 50:
        return "Любопытный котик ⭐⭐"
    elif count < 100:
        return "Котёнок, который уже ходит ⭐⭐⭐"
    else:
        return "Настоящий пушистый мудрец 🧙‍♂️🐾"

@dp.message(commands=["start", "help"])
async def start_handler(message: Message):
    await message.answer(
        "Привет, Котёнок! 🐱 Я твой уютный котик.
Выбирай, что хочешь сделать:",
        reply_markup=menu
    )

@dp.callback_query()
async def callback_handler(callback_query: types.CallbackQuery):
    user_id = str(callback_query.from_user.id)
    data = callback_query.data

    if user_id not in user_data:
        user_data[user_id] = {"cats_seen": 0}

    if data == "cat":
        photo_url = random.choice(cat_gallery)
        user_data[user_id]["cats_seen"] += 1
        save_user_data()
        await callback_query.message.answer_photo(photo_url, caption="Вот твой котёнок 🐾")
    elif data == "stats":
        count = user_data[user_id]["cats_seen"]
        rank = get_rank(count)
        await callback_query.message.answer(
            f"Ты посмотрела {count} котёнков.
Твой ранг: {rank}"
        )
    elif data == "fairy":
        tale = random.choice(fairy_tales)
        await callback_query.message.answer(
            f"<b>{tale['title']}</b>

{tale['text']}"
        )
    elif data == "gallery":
        photo_url = random.choice(cat_gallery)
        await callback_query.message.answer_photo(photo_url, caption="Уютная галерея котиков 🧸")

    await callback_query.answer()

# Webhook часть
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)
app.router.add_routes([web.post("/webhook", lambda request: setup_application(app, dp))])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    web.run_app(app, port=int(os.getenv("PORT", 8080)))
