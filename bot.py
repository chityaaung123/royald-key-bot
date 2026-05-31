import os
import time
import logging
import requests
from threading import Thread
import asyncio
from flask import Flask

app = Flask(__name__)

# မင်းရဲ့ Telegram Bot Token အသစ်
BOT_TOKEN = "8999847261:AAELT3RyDv5mw5R_LWNfGTUyT05WMTRDYts"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# /start နှုတ်ဆက်စာသား (ဒါက API သေနေလည်း ချက်ချင်း စာပြန်လာပါလိမ့်မယ်)
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

# Multi-API စနစ်ဖြင့် Link ကျော်ပေးမည့် Function
async def bypass_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_link = update.message.text
    if "http" not in user_link:
        await update.message.reply_text("❌ ကျေးဇူးပြု၍ Link အမှန်ကို ပို့ပေးပါဗျာ။")
        return

    status_msg = await update.message.reply_text("⏳ Premium Web Server ကနေ မင်းရဲ့ Key ကို ကျော်ပေးနေပါပြီ... ခဏစောင့်ပေးပါဗျာ...")
    start_time = time.time()
    
    # စမ်းသပ်မည့် API လိပ်စာ ပုံစံ ၃ ခု (အရန်စနစ် ပါဝင်သည်)
    apis = [
        f"https://api.freebypasser.xyz/api/bypass?url={user_link}",
        f"https://dl.freebypasser.xyz/api/bypass?url={user_link}",
        f"https://ethon.pylex.xyz/api/bypass?url={user_link}"
    ]
    
    success = False
    key_result = None
    link_type = "Bypass"
    
    # API တစ်ခု သေနေရင် နောက်တစ်ခုကို အလိုအလျောက် ပြောင်းစမ်းမည့် Loop စနစ်
    for api_url in apis:
        try:
            # Timeout ကို ၁၅ စက္ကန့်ပဲ ပေးထားလို့ Bot ကြီး ဟန်းမသွားတော့ပါဘူး
            response = requests.get(api_url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get("success", False) or "result" in data or "key" in data:
                    success = True
                    key_result = data.get("result") or data.get("key") or data.get("bypassed")
                    link_type = data.get("type", "Premium")
                    break # အောင်မြင်သွားရင် Loop ထဲက ထွက်မယ်
        except Exception as e:
            logging.error(f"API Error ({api_url}): {e}")
            continue # ဒီ API သေနေရင် နောက်တစ်ခုကို ဆက်စမ်းမယ်

    time_taken = round(time.time() - start_time, 2)

    if success and key_result:
        response_text = (
            f"🌟 **Bypass Success [{link_type}]**\n"
            f"🟢 Time taken {time_taken}s\n\n"
            f"**Result:**\n"
            f"`{key_result}`"
        )
        await status_msg.edit_text(response_text, parse_mode='Markdown')
    else:
        # API တွေအကုန်လုံး Down နေချိန်မှာ ပြမယ့်စာသား
        await status_msg.edit_text(
            "❌ စိတ်မကောင်းပါဘူးဗျာ၊ လက်ရှိမှာ အဓိက Bypass API Server ကြီးတွေအကုန်လုံး Down (သေ) နေလို့ပါဗျာ!\n\n"
            "Server ပြန်တက်လာရင် အလိုအလျောက် ပြန်ရပါလိမ့်မယ်။ ခဏနေမှ ထပ်စမ်းကြည့်ပေးပါဦး။"
        )

def run_tg_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    tg_app = Application.builder().token(BOT_TOKEN).build()
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bypass_link))
    
    loop.run_until_complete(tg_app.initialize())
    loop.run_until_complete(tg_app.updater.start_polling(drop_pending_updates=True))
    loop.run_until_complete(tg_app.start())
    print("🤖 Telegram Bot Is Active & Polling...")
    loop.run_forever()

@app.route("/")
def home():
    return "Royald Premium Key Bot Is Running 24/7!"

if __name__ == '__main__':
    bot_thread = Thread(target=run_tg_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
