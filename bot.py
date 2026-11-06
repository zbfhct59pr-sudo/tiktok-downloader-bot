import os
import telebot
from yt_dlp import YoutubeDL

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# معرف قناتك العامة كما هو
CHANNEL_USERNAME = "@HI709H"
CHANNEL_INVITE_LINK = "https://t.me/HI709H"

def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
    except Exception as e:
        print(f"Error checking subscription: {e}")
    return False

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if not check_subscription(user_id):
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton("اشترك في القناة للمتابعة 🚀", url=CHANNEL_INVITE_LINK)
        markup.add(btn)
        
        bot.send_message(
            message.chat.id, 
            f"عذراً، يجب عليك الاشتراك في القناة أولاً لتتمكن من استخدام البوت:\n\n{CHANNEL_USERNAME}",
            reply_markup=markup
        )
        return

    bot.reply_to(message, "أهلاً بك! أرسل لي رابط من تيك توك، إنستجرام، تويتر، أو يوتيوب وسأقوم بتحميله لك.")

@bot.message_handler(func=lambda message: True)
def download_media(message):
    user_id = message.from_user.id
    
    if not check_subscription(user_id):
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton("اشترك في القناة للمتابعة 🚀", url=CHANNEL_INVITE_LINK)
        markup.add(btn)
        
        bot.send_message(
            message.chat.id, 
            f"عذراً، يجب عليك الاشتراك في القناة أولاً لتتمكن من استخدام البوت:\n\n{CHANNEL_USERNAME}",
            reply_markup=markup
        )
        return

    url = message.text.strip()
    
    supported_domains = ["tiktok.com", "instagram.com", "twitter.com", "x.com", "youtube.com", "youtu.be"]
    if not any(domain in url for domain in supported_domains):
        bot.reply_to(message, "الرجاء إرسال رابط صحيح من تيك توك، إنستجرام، تويتر، أو يوتيوب!")
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
            info = ydl.extract
