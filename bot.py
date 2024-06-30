import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.message import ContentType

load_dotenv()

# Токен бота можно получить у https://t.me/BotFather
TOKEN = str(getenv("BOT_TOKEN"))

# Все обработчики должны быть привязаны к Роутеру (или Диспетчеру)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет!\nЭто бот для работы с гифками/демотиваторами.")

@dp.message()
async def echo_handler(message: Message) -> None:
    await message.answer("Работаем...")

# Обработчик для фото, видео и гифок
@dp.message_handler(content_types=[ContentType.PHOTO, ContentType.VIDEO, ContentType.ANIMATION])
async def media_handler(message: types.Message):
    # Создание инлайн-клавиатуры с кнопками
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="Сделать демотиватор", callback_data="make_demotivator"),
        InlineKeyboardButton(text="Получить оригинал", callback_data="get_original")
    )
    
    # Ответ с инлайн-клавиатурой
    await message.reply("Выберите действие:", reply_markup=keyboard)

# Обработчик для инлайн-кнопок
@dp.callback_query_handler(lambda c: c.data in ['make_demotivator', 'get_original'])
async def process_callback_button(callback_query: types.CallbackQuery):
    if callback_query.data == "make_demotivator":
        await callback_query.answer("Функция 'Сделать демотиватор' пока не реализована.")
    elif callback_query.data == "get_original":
        await callback_query.answer("Функция 'Получить оригинал' пока не реализована.")

async def main() -> None:
    # Инициализация экземпляра бота с настройками по умолчанию, которые будут передаваться всем API вызовам
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Запуск обработки событий
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
