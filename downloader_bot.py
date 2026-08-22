import os
import telebot
import yt_dlp

# Aapka Telegram Bot Token
TOKEN = "8852793555:AAHeGoB66uD-R0_J37z4KOsBsunag2_Xwd4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome! Instagram ya kisi aur platform ka link bhejein, video download ho jayegi.\n\n❌ *Note:* YouTube links allowed nahi hain.")

@bot.message_handler(func=lambda message: True)
def download_media(message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(message, "❌ Kripya ek valid URL (link) bhejein.")
        return

    # YouTube ko block karne ki condition
    if "youtube.com" in url or "youtu.be" in url:
        bot.reply_to(message, "❌ YouTube videos is bot se download karna band kar diya gaya hai. Kripya Instagram ya doosra link bhejein.")
        return

    msg = bot.reply_to(message, "🔍 Downloading media... Kripya intezaar karein.")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.%(ext)s',
        'noplaylist': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Video file ko Telegram par bhejna
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, caption="✅ Video downloaded successfully!")
        
        bot.delete_message(message.chat.id, msg.message_id)

        # Download hone ke baad local file delete karna
        if os.path.exists(filename):
            os.remove(filename)

    except Exception as e:
        print(e)
        bot.edit_message_text(f"❌ Error: {str(e)}", message.chat.id, msg.message_id)

print("Bot is running...")
bot.infinity_polling()
