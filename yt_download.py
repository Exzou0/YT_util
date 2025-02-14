import os
import yt_dlp
import telebot
import html
from googleapiclient.discovery import build 
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode="HTML")

def get_direct_link(video_url):
    ydl_opts = {
        'format': 'bv*+ba/b',  # Выбираем лучшее видео + аудио
        'noplaylist': True,  # Избегаем загрузки плейлистов
        'quiet': True,
        'no_warnings': True,
        'merge_output_format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)

        # Проверяем доступные форматы
        for format in info_dict.get("formats", []):
            if format.get("url") and format.get("vcodec") != "none" and format.get("acodec") != "none":
                return format["url"]

    return None  # Если видео не найдено
@bot.message_handler(func=lambda message: message.text.startswith("https://"))
def download_video(message):
    url = message.text.strip()
    direct_link = get_direct_link(url)
    if direct_link:
        text = f"🎥 Here is your video: <a href='{html.escape(direct_link)}'>Download</a>"
        bot.send_message(message.chat.id, text, parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "❌ Couldn't fetch the video link.")

if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.polling(none_stop=True)
