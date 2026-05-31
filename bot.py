import os
import time
import logging
import requests
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Flask Server အပိုင်း (Render Webhook အတွက်)
app = Flask(__name__)

BOT_TOKEN = "8952360592:AAG8r9HB4Glihm6h35n4lgNahoxt9GA0L0I"
RENDER_URL = "https://royald-key-bot.onrender.com"  # မင်းရဲ့ Render Domain Link

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Global Application variables
tg_app = None

@app.route("/", methods=["GET"])
def home():
    return "Royald Webhook Bot Is Fully Active 24/7!"

# Telegram ကနေ သတင်းအချက်အလက် လှမ်းပို့မယ့် Webhook Route
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    if tg_app:
        update = Update.de_json(request.get_json(force=True), tg_app.bot)
        # Background မှာ Update ကို ပတ်စေမယ်
        asyncio.run_coroutine_threadsafe(tg_app.process_update(update), loop)
    return "OK", 200

# /start နှုတ်ဆက်စာသား
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

# Link ကျော်ပေးမယ့် Function
async def bypass_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_link = update.message.text
    if "http" not in user_link:
        await update.message.reply_text("❌ ကျေးဇူးပြု၍ Link အမှန်ကို ပို့ပေးပါဗျာ။")
        return

    status_msg = await update.message.reply_text("⏳ Premium Web Server ကနေ မင်းရဲ့ Key ကို ကျော်ပေးနေပါပြီ... ခဏစောင့်ပေးပါဗျာ...")
    start_time = time.time()
    api_url = f"https://api.freebypasser.xyz/api/bypass?url={user_link}"
    
    try:
        response = requests.get(api_url, timeout=40)
        data = response.json()
        
        time_taken = round(time.time() - start_time, 2)
        success = data.get("success", False)
        key_result = data.get("result") or data.get("key") or data.get("bypassed")
        link_type = data.get("type", "Bypass")

        if success and key_result:
            response_text = (
                f"🌟 **Bypass Success [{link_type}]**\n"
                f"🟢 Time taken {time_taken}s\n\n"
                f"**Result:**\n"
                f"`{key_result}`"
            )
            await status_msg.edit_text(response_text, parse_mode='Markdown')
        else:
            await status_msg.edit_text("❌ စိတ်မကောင်းပါဘူးဗျာ၊ ဒီ Link က သက်တမ်းကုန်ဆုံးနေတာ (သို့မဟုတ်) ကျော်လို့ မရနိုင်တဲ့ Link ဖြစ်နေပါတယ်!")
            
    except Exception as e:
        logging.error(f"Bypass Error: {e}")
        await status_msg.edit_text("❌ API Server ဘက်က တုံ့ပြန်မှု အရမ်းကြာနေလို့ပါဗျာ။ နောက်တစ်ကြိမ် ပြန်ပို့ကြည့်ပေးပါဦး။")

async def init_webhook_bot():
    global tg_app
    tg_app = Application.builder().token(BOT_TOKEN).build()
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bypass_link))
    
    await tg_app.initialize()
    # Webhook Link ကို Telegram Server ဆီ ချိတ်ဆက်သတ်မှတ်လိုက်မယ်
    await tg_app.bot.set_webhook(url=f"{RENDER_URL}/{BOT_TOKEN}")
    await tg_app.start()
    print("🤖 Webhook Bot Configured & Connected Successfully!")

if __name__ == '__main__':
    # Background Async Loop တစ်ခု ဆောက်မယ်
    loop = asyncio.new_event_loop()
    from threading import Thread
    def start_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(init_webhook_bot())
        loop.run_forever()
        
    t = Thread(target=start_loop, args=(loop,))
    t.daemon = True
    t.start()
    
    # Flask Web Server ကို ပင်မ Thread မှာ ပွင့်စေမယ် (Render Port ချိတ်ဆက်ဖို့)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
