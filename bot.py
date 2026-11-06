import os
import telebot
from yt_dlp import YoutubeDL

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي رابط فيديو تيك توك وسأقوم بتحميله لك.")

@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    url = message.text.strip()
    
    if "tiktok.com" not in url:
        bot.reply_to(message, "الرجاء إرسال رابط تيك توك صحيح!")
        return

    msg = bot.reply_to(message, "جاري تحميل الفيديو، انتظر لحظة...")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'quiet': True,
        'nocheckcertificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        },
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video)

        if os.path.exists(filename):
            os.remove(filename)

    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء التحميل: {e}")
        
    try:
        bot.delete_message(message.chat.id, msg.message_id)
    except:
        pass

bot.infinity_polling()
