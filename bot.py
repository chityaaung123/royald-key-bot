import os
import time
import logging
import requests
from threading import Thread
import asyncio
from flask import Flask

app = Flask(__name__)

# မင်းရဲ့ Telegram Bot Token အသစ်ကို ကွက်တိထည့်ထားပါတယ်
BOT_TOKEN = "8999847261:AAELT3RyDv5mw5R_LWNfGTUyT05WMTRDYts"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# /start လို့ နှိပ်ရင် ပေါ်လာမယ့် စတိုင်ကျကျ နှုတ်ဆက်စာသား
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "🤖 **Welcome to Royald Hub Premium Bypasser!**\n\n"
        "👋 မင်္ဂလာပါဗျာ! ကျွန်တော့်ကို Lလရောက်သုံးစွဲပေးလို့ ကျေးဇူးအထူးတင်ပါတယ်ခင်ဗျာ။\n\n"
        "✨ **ထောက်ပံ့ထားသော Link များ -**\n"
        "➡️ Platoboost (Platorelay)\n"
        "➡️ Delta Key / Fluxus / Hydrogen\n"
        "➡️ Linkvertise / Link4M နှင့် အခြား Link ပေါင်း ၄၀ ကျော်\n\n"
        "⚙️ **အသုံးပြုနည်း -**\n"
        "မင်းရဲ့ Key ယူရမယ့် Link အရှည်ကြီးကို ဒီ Chat ထဲသို့ တိုက်ရိုက် Message ပို့ပေးလိုက်ပါဦးဗျာ။"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

# API ကနေ Link ကျော်ပေးမယ့် Function အစစ်
async def bypass_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_link = update.message.text
    if "http" not in user_link:
        await update.message.reply_text("❌ ကျေးဇူးပြု၍ Link အမှန်ကို ပို့ပေးပါဗျာ။")
        return

    status_msg = await update.message.reply_text("⏳ Premium Web Server ကနေ မင်းရဲ့ Key ကို ကျော်ပေးနေပါပြီ... ခဏစောင့်ပေးပါဗျာ...")
    start_time = time.time()
    
    # Premium Bypass API URL
    api_url = f"https://api.freebypasser.xyz/api/bypass?url={user_link}"
    
    try:
        # Timeout ကို 50 အထိ တိုးပေးထားပါတယ် (API ကြာရင် တုံ့ပြန်နိုင်အောင်)
        response = requests.get(api_url, timeout=50)
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

def run_tg_bot():
    # Python 3.14 နဲ့ ငြိတတ်တဲ့ run_polling စနစ်ဟောင်းနေရာမှာ စိတ်ချရတဲ့ Loop စနစ်နဲ့ ပြောင်းထားပါတယ်
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    tg_app = Application.builder().token(BOT_TOKEN).build()
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bypass_link))
    
    # Telegram ရဲ့ အမှားအဟောင်းတွေကို ရှင်းထုတ်ပြီး စက်နှိုးမယ်
    loop.run_until_complete(tg_app.initialize())
    loop.run_until_complete(tg_app.updater.start_polling(drop_pending_updates=True))
    loop.run_until_complete(tg_app.start())
    print("🤖 Telegram Bot Is Active & Polling...")
    loop.run_forever()

@app.route("/")
def home():
    return "Royald Premium Key Bot Is Running 24/7!"

if __name__ == '__main__':
    # Bot ကို Background Thread အဖြစ် ခွဲမောင်းမယ်
    bot_thread = Thread(target=run_tg_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Flask Web Server ကို ပင်မ Thread မှာ မောင်းမယ် (Render Port scan အောင်မြင်အောင်)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
