
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Кнопки
menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Хочу милого котёнка! 🐾", callback_data="cat")],
    [InlineKeyboardButton(text="Статистика 📊", callback_data="stats")],
    [InlineKeyboardButton(text="Кошачьи сказки 🌙", callback_data="fairy")],
    [InlineKeyboardButton(text="Галерея уюта 🏠", callback_data="gallery")],
])

@dp.message(commands=["start", "help"])
async def start_handler(message: Message):
    await message.answer("Привет, Котёнок! 🐱 Я твой уютный котик.
Выбирай, что хочешь сделать:", reply_markup=menu)

@dp.callback_query()
async def callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "cat":
        await callback_query.message.answer_photo("https://placekitten.com/400/300", caption="Вот твой котёнок 🐾")
    elif data == "stats":
        await callback_query.message.answer("Ты посмотрела 3 котёнка. Ранг: Маленький котёнок ⭐")
    elif data == "fairy":
        await callback_query.message.answer("Однажды котёнок лёг спать в корзинке, полной тёплого пледа... 😴")
    elif data == "gallery":
        await callback_query.message.answer_photo("https://placekitten.com/401/301", caption="Уютная галерея котиков 🧸")
    await callback_query.answer()

# Webhook часть
async def on_startup(app):
    webhook_url = os.getenv("WEBHOOK_URL")
    await bot.set_webhook(webhook_url)

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
