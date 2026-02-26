import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# توکن رباتت
TOKEN = "8116941143:AAEHkiezjL6Pht3ZmM0g8kQKmCdT_NJjcfE"

# لیست کانال‌ها
CHANNELS = [
    "@Sateki_khosh2",
    "@Sateki_khosh22",
    "@qsaie_khosh",
    "@nesteq_beserhati"
]

# FILE_ID رو بعد از گرفتن آهنگ از ربات، اینجا جایگزین کن
FILE_ID = "AgADlx8AArW8sVA"

# ساخت ربات
bot = telebot.TeleBot(TOKEN)

# ======= Handler برای گرفتن FILE_ID جدید =======
@bot.message_handler(content_types=['audio'])
def get_file_id(message):
    bot.reply_to(message, f"File ID: {message.audio.file_id}")

# ======= چک کردن عضویت کاربر در کانال‌ها =======
def check_join(user_id):
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

# ======= دستور /start =======
@bot.message_handler(commands=['start'])
def start(message):
    if check_join(message.from_user.id):
        bot.send_audio(message.chat.id, FILE_ID, caption="🎵 دانلود آهنگ آماده است!")
    else:
        markup = InlineKeyboardMarkup()
        for channel in CHANNELS:
            join_btn = InlineKeyboardButton(
                f"📢 عضویت در {channel}",
                url=f"https://t.me/{channel.replace('@','')}"
            )
            markup.add(join_btn)
        check_btn = InlineKeyboardButton("🔄 بررسی عضویت", callback_data="check")
        markup.add(check_btn)
        bot.send_message(
            message.chat.id,
            "❌ اول عضو همه کانال‌ها شو بعد بررسی کن.",
            reply_markup=markup
        )

# ======= بررسی دوباره عضویت بعد از کلیک =======
@bot.callback_query_handler(func=lambda call: call.data == "check")
def check(call):
    if check_join(call.from_user.id):
        bot.edit_message_text(
            "✅ تایید شد! در حال ارسال آهنگ...",
            call.message.chat.id,
            call.message.message_id
        )
        bot.send_audio(call.message.chat.id, FILE_ID, caption="🎵 دانلود آهنگ آماده است!")
    else:
        bot.answer_callback_query(call.id, "هنوز عضو همه کانال‌ها نشدی!")

# ======= Polling =======
bot.infinity_polling()
