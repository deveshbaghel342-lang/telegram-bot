import os
import telebot
import yt_dlp

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

def download_instagram(url):
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': 'best',
        'cookiefile': 'cookies.txt'  # optional, for private content
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
        return file_path, info.get('ext')

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Send me any Instagram reel/post/story link!")

@bot.message_handler(func=lambda msg: True)
def handle_url(message):
    url = message.text
    try:
        file_path, ext = download_instagram(url)
        with open(file_path, 'rb') as f:
            if ext in ['mp4', 'mkv', 'webm']:
                bot.send_video(message.chat.id, f)
            else:
                bot.send_photo(message.chat.id, f)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

bot.polling()
