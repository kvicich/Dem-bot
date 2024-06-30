import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

load_dotenv()

# Токен бота можно получить на https://t.me/BotFather
TOKEN = str(getenv("BOT_TOKEN"))

# Все обработчики должны быть привязаны к Роутеру (или Диспетчеру)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет!\nЭто бот для работы с гифками/демотиваторами.")

@dp.message()
async def echo_handler(message: Message) -> None:
    await message.answer("Работаем...")

async def main() -> None:
    # Инициализация экземпляра бота с настройками по умолчанию, которые будут передаваться всем API вызовам
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Запуск обработки событий
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
