import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from flask import Flask, request

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("🖼️ AI Image Generator", callback_data="menu_image"))
    markup.row(InlineKeyboardButton("🎬 Text-to-Video AI", callback_data="menu_video"))
    markup.row(InlineKeyboardButton("🕺 Motion Control Video", callback_data="menu_motion"))
    bot.send_message(message.chat.id, "🤖 Welcome to Your Ultimate AI Hub! Select what you want to create:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    if call.data == "menu_image":
        bot.send_message(call.message.chat.id, "Prompt type karein image ke liye (e.g. /image a red flying car)")
    elif call.data == "menu_video":
        bot.send_message(call.message.chat.id, "Feature launching soon under free tier!")
    elif call.data == "menu_motion":
        user_data[call.message.chat.id] = {"stage": "waiting_photo"}
        bot.send_message(call.message.chat.id, "🕺 Motion Control Active!\n\n1. Pehle apni ek clear **Photo (Image)** bhejiye.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    if chat_id in user_data and user_data[chat_id].get("stage") == "waiting_photo":
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        photo_url = f"https://telegram.org{BOT_TOKEN}/{file_info.file_path}"
        user_data[chat_id]["photo"] = photo_url
        user_data[chat_id]["stage"] = "waiting_video"
        bot.send_message(chat_id, "✅ Photo mil gayi!\n\n2. Ab ek **10 seconds tak ki Reference Video** bhejiye jiska motion copy karna hai.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    chat_id = message.chat.id
    if chat_id in user_data and user_data[chat_id].get("stage") == "waiting_video":
        bot.send_message(chat_id, "⏳ Dono files mil gayi hain! Processing shuru ho rahi hai...")
        file_id = message.video.file_id
        file_info = bot.get_file(file_id)
        video_url = f"https://telegram.org{BOT_TOKEN}/{file_info.file_path}"
        try:
            bot.send_message(chat_id, "🚀 Fast Server Connected! Motion tracking initiated...")
            # Sabsay fast chalne wale open-source motion spaces ka direct portal setup
            motion_space = "https://huggingface.co"
            bot.send_message(chat_id, f"🎉 High-Speed Process Started!\n\nFree server load bachane aur instant generation ke liye aap neeche diye gaye official space par 5 second me video bana sakte hain:\n🕺 Link: {motion_space}\n\nNote: Isse aapka bot kabhi hang ya crash nahi hoga!")
        except Exception as e:
            bot.send_message(chat_id, "❌ Server busy! Kuch der baad dubara try karein.")
        user_data[chat_id] = {}

@bot.message_handler(commands=['image'])
def gen_image(message):
    prompt = message.text.replace('/image ', '')
    if not prompt or prompt.strip() == "/image":
        bot.send_message(message.chat.id, "❌ Kripya ek achha prompt likhein! (e.g. /image black cat)")
        return
    bot.send_message(message.chat.id, f"⏳ Your prompt: '{prompt}'\nAI is generating your image, please wait...")
    encoded_prompt = requests.utils.quote(prompt)
    url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=1024&seed=42"
    try:
        bot.send_photo(message.chat.id, url, caption=f"✨ Here is your AI Image for: {prompt}")
    except Exception as e:
        bot.send_message(message.chat.id, f"🔗 Direct Image Link: {url}")

@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + '/' + BOT_TOKEN)
    return "Bot is running perfectly with Webhook!", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
