import os
import yt_dlp
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Function to download audio from a YouTube link
def download_audio(message):
    url = message.text.strip()  # Extract the text message and remove extra spaces
    chat_id = message.chat.id  # Get the chat ID to send responses

    # Validate if the message contains a correct YouTube link
    if not (url.startswith("http://") or url.startswith("https://")) or "youtube.com" not in url and "youtu.be" not in url:
        bot.send_message(chat_id, "❌ Send the correct YouTube link!")  # Send an error message if the link is invalid
        return

    # Configuration options for yt-dlp
    opts = {
        "format": "bestaudio/best",  # Download the best available audio format
        "outtmpl": "%(title)s.%(ext)s",  # File name will be the video title with its original extension
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)  # Fetch video info and download the file
            file = ydl.prepare_filename(info)  # Get the downloaded file's name

        # Open the downloaded file and send it as an audio message
        with open(file, "rb") as audio:
            bot.send_audio(chat_id, audio)

        os.remove(file)  # Delete the file after sending to free up space

    except Exception as e:
        bot.send_message(chat_id, f"❌ Download Error: {e}")  # Send an error message in case of failure

# Run the bot
if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.polling(none_stop=True)  # Start the bot in polling mode
