import os
import yt_dlp #библиотека для загрузки видео
import telebot
from dotenv import load_dotenv

# Загрузка переменных из файла .env
load_dotenv()

# Получение токена
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode="HTML")

# Функция для загрузки аудио из YouTube-ссылки
def download_audio(message):
    url = message.text.strip()  # Извлекаем текст сообщения и убираем лишние пробелы
    chat_id = message.chat.id  # Получаем ID чата для отправки ответа

    # Проверяем, содержит ли сообщение корректную YouTube-ссылку
    if not (url.startswith("http://") or url.startswith("https://")) or "youtube.com" not in url and "youtu.be" not in url:
        bot.send_message(chat_id, "❌ Send the correct YouTube link!")  # Отправляем сообщение об ошибке если ссылка ошибочна
        return

    # настройки yt-dlp для загрузки аудио
    opts = {
        "format": "bestaudio/best",  # лучший доступный аудиоформат
        "outtmpl": "%(title)s.%(ext)s",  # Сохраняем файл с названием видео и оригинальным расширением
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)  # Получаем информацию о видео и загружаем файл
            file = ydl.prepare_filename(info)  # Получаем имя загруженного файла

        # Открываем загруженный файл и отправляем его как аудиосообщение
        with open(file, "rb") as audio:
            bot.send_audio(chat_id, audio)

        os.remove(file)  # Удаляем файл после отправки

    except Exception as e:
        bot.send_message(chat_id, f"❌ Download Error: {e}")  # сообщение об ошибке 

if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.polling(none_stop=True)  # Запускаем бота в непрерывном режиме
