import os
import telebot # для работы с Telegram API
import html # обработка HTML-символов в текстах
from telebot.types import ReplyKeyboardMarkup, KeyboardButton # классы для работы с клавиатурой бота (кнопки, разметка)
from googleapiclient.discovery import build # для работы с YouTube API (поиск видео)
from dotenv import load_dotenv
from yt_download import download_video
from yt_conv import download_audio

# Загружаем переменные 
load_dotenv()

# Получаем API-ключи 
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode="HTML") #позволяет использовать HTML-разметку в сообщениях

#  главное меню
def main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🔍 Search by query"))
    keyboard.add(KeyboardButton("🎵 Convert to MP3"))
    keyboard.add(KeyboardButton("📥 Download video"))
    return keyboard

# Функция поиска видео на YouTube
def search_youtube(query):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY) # подключаемся к YouTube API
    request = youtube.search().list(  # отправляем запрос к API для поиска видео
        q=query, part="snippet", type="video", maxResults=5
    )
    response = request.execute()
    
    videos = []
    for item in response.get("items", []): # генерируем список найденных видео в формате HTML
        video_id = item["id"]["videoId"]
        title = html.escape(item["snippet"]["title"]) 
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append(f"🎬 <b>{title}</b>\n🔗 {video_url}")
    
    return "\n\n".join(videos) if videos else "❌ No video found." #формирует список видео для отправки

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Choose an action:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "🔍 Search by query")
def handle_search(message):
    bot.send_message(message.chat.id, "Enter your search query:")
    bot.register_next_step_handler(message, process_search)

# Обработка поискового запроса
def process_search(message):
    query = message.text.strip() # получаем текст запроса
    if query:
        bot.send_message(message.chat.id, "🔎 Searching for videos... ⏳")
        videos = search_youtube(query)
        bot.send_message(message.chat.id, videos)
    else:
        bot.send_message(message.chat.id, "⚠ Please enter a text query!")

@bot.message_handler(func=lambda message: message.text == "📥 Download video")
def handle_download_video(message):
    bot.send_message(message.chat.id, "Send the YouTube video link:")
    bot.register_next_step_handler(message, download_video)

@bot.message_handler(func=lambda message: message.text == "🎵 Convert to MP3")
def handle_download_audio(message):
    bot.send_message(message.chat.id, "Send the YouTube video link.")
    bot.register_next_step_handler(message, download_audio)

# Запуск бота
if __name__ == "__main__": # если файл запущен напрямую, запускаем бота
    print("🤖 Bot is running...")
    bot.polling(none_stop=True) # бот работает без остановки
