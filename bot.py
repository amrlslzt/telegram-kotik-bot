from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

API_TOKEN = "7812132389:AAHsNiYnCXDnmDYAD9MOpuIXg0FaGWLGzSU"

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Главное меню
def get_main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="🐱 Хочу милого котёнка!", callback_data="cute_cat")
    kb.button(text="🎥 Котик на камеру", callback_data="cat_video")
    kb.button(text="🌙 Котик дня по настроению", callback_data="mood_cat")
    kb.button(text="📖 Кошачьи сказки", callback_data="fairy_tale")
    kb.button(text="🧘 Кото-медитации", callback_data="meditation")
    kb.button(text="😴 Сонный котик (АСМР)", callback_data="asmr")
    kb.button(text="⏰ Котик по расписанию", callback_data="schedule")
    kb.button(text="📝 Котик рекомендует", callback_data="recommend")
    kb.button(text="📸 Галерея уюта", callback_data="gallery")
    kb.button(text="⭐ Статистика", callback_data="stats")
    kb.button(text="🎀 Лист желаний", callback_data="wishlist")
    return kb.as_markup(resize_keyboard=True)

@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        f"Привет, Котёнок! 🐾\nЯ твой уютный котик. Нажимай кнопки и расслабляйся.",
        reply_markup=get_main_menu()
    )

@dp.callback_query()
async def menu_handler(callback: CallbackQuery):
    action = callback.data
    await callback.answer()
    await callback.message.answer(f"🐾 Ты выбрала: {action} (пока функция в разработке)")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
