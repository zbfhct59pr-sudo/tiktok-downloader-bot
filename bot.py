import os
import telebot
from yt_dlp import YoutubeDL

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

CHANNEL_INVITE_LINK = "https://t.me/+KB8JInbcu405ZDg8"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn_channel = telebot.types.InlineKeyboardButton("اضغط هنا للانضمام للقناة 🚀", url=CHANNEL_INVITE_LINK)
    btn_check = telebot.types.InlineKeyboardButton("تحقق من انضمامك ✅", callback_data="check_sub")
    markup.add(btn_channel)
    markup.add(btn_check)
    
    bot.send_message(
        message.chat.id, 
        "أهلاً بك! لتحميل مقاطع الفيديو، يجب عليك الانضمام للقناة الخاصة أولاً.\n\nاضغط على زر الانضمام، ثم اضغط على زر التحقق بالأسفل:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def download_media(message):
    url = message.text.strip()
    
    supported_domains = ["tiktok.com", "instagram.com", "twitter.com", "x.com", "youtube.com", "youtu.be"]
    if not any(domain in url for domain in supported_domains):
        markup = telebot.types.InlineKeyboardMarkup()
        btn_channel = telebot.types.InlineKeyboardButton("قناتنا الخاصة 🚀", url=CHANNEL_INVITE_LINK)
        btn_check = telebot.types.InlineKeyboardButton("تحقق من انضمامك ✅", callback_data="check_sub")
        markup.add(btn_channel, btn_check)
        
        bot.reply_to(message, "الرجاء الانضمام للقناة أولاً ثم إرسال الرابط الصحيح (تيك توك، انستجرام، إلخ).", reply_markup=markup)
        return

    msg = bot.reply_to(message, "جاري معالجة وتحميل المحتوى، انتظر لحظة...")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'quiet': True,
        'nocheckcertificate': True,
        'extractor_args': {
            'tiktok': {
                'app_version': ['30.4.0'],
                'api_hostname': ['api16-normal-c-useast1a.tiktokv.com']
            }
        },
    }

    filename = None
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video)

    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء التحميل: {
