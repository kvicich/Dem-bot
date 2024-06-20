import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import os

# Установите уровень логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Устанавливаем middleware для логирования
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я твой новый бот.")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Как я могу помочь?")

@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(message.text)

def get_token():
    token_directory = os.path.dirname(os.path.abspath(__file__))
    token_file_path = os.path.join(token_directory, "TOKEN.txt")
    if os.path.exists(token_file_path):
        try:
            with open(token_file_path, "r") as file:
                token = file.read().strip()
                if token:
                    return token
                else:
                    logger.error("Токен не найден в файле TOKEN.txt")
                    return None
        except Exception as e:
            logger.error(f"Ошибка при чтении токена из файла: {e}")
            return None
    else:
        logger.error("Файл TOKEN.txt не найден")
        TOKEN = input("Введите токен: ")
        with open(token_file_path, 'w') as file:
            file.write(TOKEN)
        return TOKEN

def main():
    # Получение токена
    API_TOKEN = get_token()
    if not API_TOKEN:
        raise ValueError("Не удалось получить токен для бота")
    
    # Создаем объекты бота и диспетчера
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)

    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()
