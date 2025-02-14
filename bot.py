import os
import telebot
import html
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from googleapiclient.discovery import build
from dotenv import load_dotenv
from yt_download import download_video
from yt_conv import download_audio

# Load environment variables
load_dotenv()

# Retrieve API keys from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Initialize the bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode="HTML")

# Create the main menu keyboard
def main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🔍 Search by query"))
    keyboard.add(KeyboardButton("🎵 Convert to MP3"))
    keyboard.add(KeyboardButton("📥 Download video"))
    return keyboard

# Function to search videos on YouTube
def search_youtube(query):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        q=query, part="snippet", type="video", maxResults=5
    )
    response = request.execute()
    
    videos = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        title = html.escape(item["snippet"]["title"])
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append(f"🎬 <b>{title}</b>\n🔗 {video_url}")
    
    return "\n\n".join(videos) if videos else "❌ No video found."

# Handle /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Choose an action:", reply_markup=main_menu())

# Handle "🔍 Search by query" button
@bot.message_handler(func=lambda message: message.text == "🔍 Search by query")
def handle_search(message):
    bot.send_message(message.chat.id, "Enter your search query:")
    bot.register_next_step_handler(message, process_search)

# Process search query
def process_search(message):
    query = message.text.strip()
    if query:
        bot.send_message(message.chat.id, "🔎 Searching for videos... ⏳")
        videos = search_youtube(query)
        bot.send_message(message.chat.id, videos)
    else:
        bot.send_message(message.chat.id, "⚠ Please enter a text query!")

# Handle "📥 Download video" button
@bot.message_handler(func=lambda message: message.text == "📥 Download video")
def handle_download_video(message):
    bot.send_message(message.chat.id, "Send the YouTube video link:")
    bot.register_next_step_handler(message, download_video)

# Handle "🎵 Convert to MP3" button
@bot.message_handler(func=lambda message: message.text == "🎵 Convert to MP3")
def handle_download_audio(message):
    bot.send_message(message.chat.id, "Send the YouTube video link.")
    bot.register_next_step_handler(message, download_audio)

# Start the bot
if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.polling(none_stop=True)