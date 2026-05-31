import os
import time
import logging
import requests
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Flask Web Server အပိုင်း
app = Flask(__name__)

@app.route("/")
def home():
    return "Royald Bot Is Fully Active 24/7!"

# Telegram Bot အပိုင်း
BOT_TOKEN = "8152360592:AAG8n9Hb4G1ihm6h35n4lNahokt9GAOLOI"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

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

async def run_bot():
    # Application ကို တိုက်ရိုက် ဆောက်မယ်
    tg_app = Application.builder().token(BOT_TOKEN).build()
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bypass_link))
    
    # Python 3.14 နဲ့ ငြိနေတဲ့ run_polling() အစား အခြေခံကျကျ စနစ်နဲ့ ပွင့်စေတာပါ
    await tg_app.initialize()
    await tg_app.updater.start_polling()
    await tg_app.start()
    print("🤖 Telegram Bot Started Successfully!")
    
    # Flask Server ကို တွဲလျက် Run ပေးထားမယ်
    port = int(os.environ.get("PORT", 5000))
    from werkzeug.serving import make_server
    server = make_server('0.0.0.0', port, app)
    
    # Bot ရော Flask ရော မပိတ်ဘဲ ၂၄ နာရီပတ်လုံး ပွင့်နေစေမယ့် Loop
    while True:
        server.handle_request()
        await asyncio.sleep(0.1)

if __name__ == '__main__':
    # စနစ်သစ်အရ ကွင်းဆက်တစ်ခုလုံးကို ခေါ်ယူပွင့်စေတာပါ
    asyncio.run(run_bot())
