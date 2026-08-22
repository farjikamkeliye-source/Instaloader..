import telebot
import yt_dlp
import os
import uuid
from flask import Flask
from threading import Thread

TOKEN = "8852793555:AAHeGoB66uD-R0_J37z4KOsBsunag2_Xwd4"
bot = telebot.TeleBot(TOKEN)

# Web server taaki Render ka Port Binding error fix ho jaye
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if not os.path.exists('downloads'):
    os.makedirs('downloads')

def download_media(url):
    unique_name = str(uuid.uuid4())
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'downloads/{unique_name}.%(ext)s',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f"👋 Hi {message.from_user.first_name}!\n\nMain 24/7 Cloud par live hoon. Koi bhi link bhejo, download karke dunga.")

@bot.message_handler(func=lambda message: True)
def handle_link(message):
    url = message.text.strip()
    if not url.startswith("http"):
        return

    wait_msg = bot.reply_to(message, "⏳ Downloading... thoda rukiye.")
    
    try:
        file_path = download_media(url)
        with open(file_path, 'rb') as f:
            if file_path.endswith(('.mp4', '.mkv', '.webm')):
                bot.send_video(message.chat.id, f, caption="✅ Downloaded successfully!")
            else:
                bot.send_photo(message.chat.id, f, caption="✅ Downloaded successfully!")
        os.remove(file_path)
        bot.delete_message(message.chat.id, wait_msg.message_id)
    except Exception as e:
        try:
            bot.delete_message(message.chat.id, wait_msg.message_id)
        except:
            pass
        bot.reply_to(message, f"❌ Error: {e}")

if __name__ == "__main__":
    # Web server ko background mein chalana
    t = Thread(target=run_web)
    t.start()
    
    print("🚀 Cloud Bot is starting...")
    bot.infinity_polling(skip_pending=True)
  
