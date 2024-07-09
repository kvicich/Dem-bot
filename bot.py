import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import Command
from aiogram.types import Message
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mpy
import tempfile
import os

load_dotenv()

# Токен бота можно получить у https://t.me/BotFather
TOKEN = str(getenv("BOT_TOKEN"))

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

# Установка parse_mode после инициализации бота
bot.parse_mode = ParseMode.HTML

@router.message(Command(commands=['demik']))
async def command_demik_handler(message: Message) -> None:
    # Проверка наличия ответа на сообщение с медиафайлом
    if message.reply_to_message and (message.reply_to_message.photo or message.reply_to_message.video or message.reply_to_message.animation):
        command_args = message.text.split(maxsplit=1)
        caption = command_args[1] if len(command_args) > 1 else ""
        if not caption:
            await message.answer("Пожалуйста, укажите текст для подписи после запятой.")
        else:
            await process_media(message.reply_to_message, caption)
    elif (message.photo or message.video or message.animation) and message.caption:
        await process_media(message, message.caption)
    else:
        await message.answer("Отправьте фото/видео/гифку с подписью через запятую или используйте команду как ответ на фото/видео/гифку.")

async def process_media(message: Message, caption: str) -> None:
    if not caption:
        await message.reply("Пожалуйста, укажите текст для подписи после запятой.")
        return

    demotivator_text = caption.strip()

    if message.content_type == ContentType.PHOTO:
        file_info = await bot.get_file(message.photo[-1].file_id)
        file_path = file_info.file_path
        downloaded_file = await bot.download_file(file_path)
        with open(f"temp_{message.photo[-1].file_id}.jpg", 'wb') as new_file:
            new_file.write(downloaded_file.getvalue())
        demotivator_path = create_demotivator_image(new_file.name, demotivator_text)
    elif message.content_type == ContentType.VIDEO:
        file_info = await bot.get_file(message.video.file_id)
        file_path = file_info.file_path
        downloaded_file = await bot.download_file(file_path)
        with open(f"temp_{message.video.file_id}.mp4", 'wb') as new_file:
            new_file.write(downloaded_file.getvalue())
        demotivator_path = create_demotivator_video(new_file.name, demotivator_text)
    elif message.content_type == ContentType.ANIMATION:
        file_info = await bot.get_file(message.animation.file_id)
        file_path = file_info.file_path
        downloaded_file = await bot.download_file(file_path)
        with open(f"temp_{message.animation.file_id}.gif", 'wb') as new_file:
            new_file.write(downloaded_file.getvalue())
        demotivator_path = create_demotivator_gif(new_file.name, demotivator_text)
    
    with open(demotivator_path, 'rb') as demotivator_media:
        await bot.send_document(message.chat.id, demotivator_media)
    
    os.remove(demotivator_path)
    if message.content_type == ContentType.PHOTO:
        os.remove(f"temp_{message.photo[-1].file_id}.jpg")
    elif message.content_type == ContentType.VIDEO:
        os.remove(f"temp_{message.video.file_id}.mp4")
    elif message.content_type == ContentType.ANIMATION:
        os.remove(f"temp_{message.animation.file_id}.gif")

def create_demotivator_image(image_path, text):
    image = Image.open(image_path)
    width, height = image.size
    new_height = height + 100
    new_image = Image.new('RGB', (width, new_height), (0, 0, 0))
    new_image.paste(image, (0, 0))

    draw = ImageDraw.Draw(new_image)
    font = ImageFont.load_default()
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (width - text_width) / 2
    text_y = height + 20
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

    temp_image_path = tempfile.mktemp(suffix=".jpg")
    new_image.save(temp_image_path)

    clip = mpy.ImageClip(temp_image_path).set_duration(5)
    temp_gif_path = tempfile.mktemp(suffix=".gif")
    clip.write_gif(temp_gif_path, fps=10)

    os.remove(temp_image_path)
    
    return temp_gif_path

def create_demotivator_video(video_path, text):
    video_clip = mpy.VideoFileClip(video_path)
    width, height = video_clip.size

    txt_clip = mpy.TextClip(text, fontsize=24, color='white', size=(width, None), method='caption', bg_color='black')
    txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(video_clip.duration)

    result = mpy.CompositeVideoClip([video_clip, txt_clip])

    temp_video_path = tempfile.mktemp(suffix=".mp4")
    result.write_videofile(temp_video_path, codec='libx264', fps=24)

    return temp_video_path

def create_demotivator_gif(gif_path, text):
    gif_clip = mpy.VideoFileClip(gif_path)
    width, height = gif_clip.size

    txt_clip = mpy.TextClip(text, fontsize=24, color='white', size=(width, None), method='caption', bg_color='black')
    txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(gif_clip.duration)

    result = mpy.CompositeVideoClip([gif_clip, txt_clip])

    temp_gif_path = tempfile.mktemp(suffix=".gif")
    result.write_gif(temp_gif_path, fps=gif_clip.fps)

    return temp_gif_path

dp.include_router(router)

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
