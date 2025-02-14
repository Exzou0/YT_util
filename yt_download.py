import os
import yt_dlp #библиотека для загрузки видео.
import telebot
import html
from dotenv import load_dotenv

load_dotenv()

# Получаем API-ключи
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode="HTML")

# Функция для получения прямой ссылки на скачивание видео
def get_direct_link(video_url):
    ydl_opts = {
        'format': 'bv*+ba/b',  # Выбор лучшего формата видео + аудио
        'noplaylist': True,  # Запрет загрузки плейлистов
        'quiet': True,  # Отключение вывода логов
        'no_warnings': True,  # Ignore warnings
        'merge_output_format': 'mp4'  #  вывод в формате MP4
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)  # Получение информации о видео без загрузки

        # Проверка доступных форматов
        for format in info_dict.get("formats", []):
            # Проверка, что формат содержит как видео, так и аудио
            if format.get("url") and format.get("vcodec") != "none" and format.get("acodec") != "none":
                return format["url"]  # Возвращение прямого URL видео

    return None  # Return None if no valid video format is found

# Обработчик сообщений содержащих ссылку на YouTube
@bot.message_handler(func=lambda message: message.text.startswith("https://"))
def download_video(message):
    url = message.text.strip()  # # Извлечение и очистка URL из сообщения
    direct_link = get_direct_link(url)  # Получение прямой ссылки на скачивание

    if direct_link:
        text = f"🎥 Here is your video: <a href='{html.escape(direct_link)}'>Download</a>"
        bot.send_message(message.chat.id, text, parse_mode="HTML")  # Отправка ссылки на скачивание пользователю
    else:
        bot.send_message(message.chat.id, "❌ Couldn't fetch the video link.")  # Send an error message if failed

if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.polling(none_stop=True)  # Запуск непрерывного получения новых сообщений
