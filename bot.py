import os
import time
import logging
import requests
from threading import Thread
from flask import Flask
import telebot

# Flask Web Server အပိုင်း
app = Flask(__name__)

@app.route("/")
def home():
    return "Royald Premium Bot Is Active 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# Telegram Bot အပိုင်း (မင်းရဲ့ Bot Token အသစ်)
BOT_TOKEN = "8999847261:AAELT3RyDv5mw5R_LWNfGTUyT05WMTRDYts"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="MARKDOWN")

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# /start နှုတ်ဆက်စာသား
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🤖 **Welcome to Royald Hub Premium Bypasser!**\n\n"
        "👋 မင်္ဂလာပါဗျာ! ကျွန်တော့်ကို လာရောက်သုံးစွဲပေးလို့ ကျေးဇူးအထူးတင်ပါတယ်ခင်ဗျာ။\n\n"
        "✨ **ထောက်ပံ့ထားသော Link များ -**\n"
        "➡️ Platoboost (Platorelay)\n"
        "➡️ Delta Key / Fluxus / Hydrogen\n"
        "➡️ Linkvertise / Link4M နှင့် အခြား Link ပေါင်း ၄၀ ကျော်\n\n"
        "⚙️ **အသုံးပြုနည်း -**\n"
        "မင်းရဲ့ Key ယူရမယ့် Link အရှည်ကြီးကို ဒီ Chat ထဲသို့ တိုက်ရိုက် Message ပို့ပေးလိုက်ပါဦးဗျာ။"
    )
    bot.reply_to(message, welcome_text)

# Link ကျော်ပေးမယ့် Function
@bot.message_handler(func=lambda message: True)
def bypass_link(message):
    user_link = message.text
    if "http" not in user_link:
        bot.reply_to(message, "❌ ကျေးဇူးပြု၍ Link အမှန်ကို ပို့ပေးပါဗျာ။")
        return

    status_msg = bot.reply_to(message, "⏳ Premium Web Server ကနေ မင်းရဲ့ Key ကို ကျော်ပေးနေပါပြီ... ခဏစောင့်ပေးပါဗျာ...")
    start_time = time.time()
    
    apis = [
        f"https://api.freebypasser.xyz/api/bypass?url={user_link}",
        f"https://dl.freebypasser.xyz/api/bypass?url={user_link}",
        f"https://ethon.pylex.xyz/api/bypass?url={user_link}"
    ]
    
    success = False
    key_result = None
    link_type = "Bypass"
    
    for api_url in apis:
        try:
            response = requests.get(api_url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get("success", False) or "result" in data or "key" in data:
                    success = True
                    key_result = data.get("result") or data.get("key") or data.get("bypassed")
                    link_type = data.get("type", "Premium")
                    break
        except Exception as e:
            logging.error(f"API Error ({api_url}): {e}")
            continue

    time_taken = round(time.time() - start_time, 2)

    if success and key_result:
        response_text = (
            f"🌟 **Bypass Success [{link_type}]**\n"
            f"🟢 Time taken {time_taken}s\n\n"
            f"**Result:**\n"
            f"`{key_result}`"
        )
        bot.edit_message_text(response_text, chat_id=message.chat.id, message_id=status_msg.message_id)
    else:
        bot.edit_message_text(
            "❌ စိတ်မကောင်းပါဘူးဗျာ၊ လက်ရှိမှာ အဓိက Bypass API Server ကြီးတွေအကုန်လုံး Down (သေ) နေလို့ပါဗျာ!\n\n"
            "Server ပြန်တက်လာရင် အလိုအလျောက် ပြန်ရပါလိမ့်မယ်။ ခဏနေမှ ထပ်စမ်းကြည့်ပေးပါဦး။",
            chat_id=message.chat.id, message_id=status_msg.message_id
        )

if __name__ == '__main__':
    # 1. Flask ကို Background Thread နဲ့ Run ထားမယ်
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # 2. 🔥 Webhook အဟောင်းတွေကို လုံးဝ အပြတ်ရှင်းထုတ်ပစ်မယ့် အပိုင်း (ဒါကြောင့် စာပြန်လာမှာပါ)
    print("🧹 Removing old webhooks...")
    bot.remove_webhook()
    time.sleep(1)
    
    # 3. Telebot ကို အသစ်စက်စက် Polling စမောင်းမယ်
    print("🤖 Telebot is starting via Polling...")
    bot.infinity_polling(skip_pending_updates=True)
