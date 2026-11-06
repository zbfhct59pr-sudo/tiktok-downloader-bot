import os
import telebot
import requests
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
    
    filename = "video.mp4"
    success = False

    try:
        # إذا كان الرابط تيك توك، نستخدم واجهة بديلة سريعة لتجاوز حظر السيرفرات
        if "tiktok.com" in url:
            api_url = f"https://tikwm.com/api/?url={url}"
            res = requests.get(api_url).json()
            if res.get("code") == 0:
                video_url = res["data"]["play"]
                video_data = requests.get(video_url).content
                with open(filename, "wb") as f:
                    f.write(video_data)
                success = True
        
        # لباقي المنصات نستخدم YoutubeDL العادي
        if not success:
            ydl_opts = {
                'format': 'best',
                'outtmpl': filename,
                'quiet': True,
                'nocheckcertificate': True,
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            success = True

        if success and os.path.exists(filename):
            with open(filename, 'rb') as video:
                bot.send_video(message.chat.id, video)

    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء التحميل: {e}")
        
    finally:
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass
        
        try:
            bot.delete_message(message.chat.id, msg.message_id)
        except:
            pass

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_check(call):
    bot.answer_callback_query(call.id, "تم التحقق بنجاح! يمكنك الآن إرسال الروابط وتحميلها.")
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="أنت جاهز الآن! أرسل لي أي رابط
