import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "توکن_ربات"

CHANNELS = [
    "@Sateki_khosh2",
    "@Sateki_khosh22",
    "@qsaie_khosh",
    "@nesteq_beserhati"
]

bot = telebot.TeleBot(TOKEN)

last_file_id = None


# چک عضویت
def check_join(user_id):
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ["member","administrator","creator"]:
                return False
        except:
            return False
    return True


# استارت
@bot.message_handler(commands=['start'])
def start(message):
    global last_file_id

    if not last_file_id:
        bot.send_message(message.chat.id,"❌ هنوز آهنگی تنظیم نشده")
        return

    if check_join(message.from_user.id):
        bot.send_audio(message.chat.id,last_file_id,caption="🎧 دانلود آهنگ")
    else:
        markup = InlineKeyboardMarkup()

        for channel in CHANNELS:
            markup.add(
                InlineKeyboardButton(
                    "عضویت در کانال",
                    url=f"https://t.me/{channel.replace('@','')}"
                )
            )

        markup.add(
            InlineKeyboardButton("✅ بررسی عضویت",callback_data="check")
        )

        bot.send_message(
            message.chat.id,
            "اول در کانال‌ها عضو شو بعد بررسی بزن 👇",
            reply_markup=markup
        )


# دکمه بررسی
@bot.callback_query_handler(func=lambda call: call.data=="check")
def check(call):
    global last_file_id

    if check_join(call.from_user.id):
        bot.send_audio(call.message.chat.id,last_file_id,caption="🎧 دانلود آهنگ")
    else:
        bot.answer_callback_query(call.id,"❌ هنوز عضو نشدی")


# وقتی ادمین آهنگ بفرستد
@bot.message_handler(content_types=['audio'])
def save_audio(message):
    global last_file_id

    last_file_id = message.audio.file_id
    bot.send_message(message.chat.id,"✅ آهنگ ذخیره شد")


bot.infinity_polling()
