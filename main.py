import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

# Token setup directly from environment
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.environ.get("HUGGING_FACE_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

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
        bot.send_message(call.message.chat.id, "Motion control ke liye pehle apni photo bheinjein, fir reference video!")

@bot.message_handler(commands=['image'])
def gen_image(message):
    prompt = message.text.replace('/image ', '')
    bot.send_message(message.chat.id, "⏳ Generating your image...")
    url = f"https://pollinations.ai{prompt}"
    bot.send_photo(message.chat.id, url)

# Fake background loop to keep server alive
from flask import Flask
app = Flask('')
@app.route('/')
def home(): return "Bot is running!"

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    bot.infinity_polling()
