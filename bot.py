import os
import telebot
from yt_dlp import YoutubeDL

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي رابط فيديو من TikTok وسيتم تحميله فوراً 🎬")

@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    url = message.text.strip()

    if "tiktok.com" not in url:
        bot.reply_to(message, "يرجى إرسال رابط تيك توك صحيح.")
        return

    msg = bot.reply_to(message, "جاري تحميل الفيديو، انتظر لحظة... ⏳")

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'video.%(ext)s',
        'quiet': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, reply_to_message_id=message.message_id)

        if os.path.exists(filename):
            os.remove(filename)

        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"حدث خطأ أثناء التحميل: {str(e)}", message.chat.id, msg.message_id)

bot.infinity_polling()
