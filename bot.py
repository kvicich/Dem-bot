import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData

load_dotenv()

# Токен бота можно получить у https://t.me/BotFather
TOKEN = str(getenv("BOT_TOKEN"))

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()

# Создание callback_data для кнопок
callback_data = CallbackData("action", "type")

# Обработчик команды /start
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Привет!\nЭто бот для работы с гифками/демотиваторами.")

# Обработчик для фото, видео и гифок
@router.message(F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO, ContentType.ANIMATION]))
async def media_handler(message: Message):
    # Создание инлайн-клавиатуры с кнопками
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="Сделать демотиватор", callback_data=callback_data.new(type="make_demotivator")),
        InlineKeyboardButton(text="Получить оригинал", callback_data=callback_data.new(type="get_original"))
    )
    
    # Ответ с инлайн-клавиатурой
    await message.reply("Выберите действие:", reply_markup=keyboard)

# Обработчик для инлайн-кнопок
@router.callback_query(callback_data.filter(F.type.in_(["make_demotivator", "get_original"])))
async def process_callback_button(callback_query: CallbackQuery, callback_data: dict):
    if callback_data['type'] == "make_demotivator":
        await callback_query.answer("Функция 'Сделать демотиватор' пока не реализована.")
    elif callback_data['type'] == "get_original":
        await callback_query.answer("Функция 'Получить оригинал' пока не реализована.")

# Регистрация роутера
dp.include_router(router)

async def main() -> None:
    # Запуск обработки событий
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
