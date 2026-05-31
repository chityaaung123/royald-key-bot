import os
import logging
import requests
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)

# မင်းရဲ့ Telegram Bot Token ကို ဒီမှာ ထည့်ပေးပါဦး
BOT_TOKEN = os.getenv("8952360592:AAG8r9HB4Glihm6h35n4lgNahoxt9GA0L0I")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
tg_app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 မင်္ဂလာပါဗျာ! Royald Hub Key Bypasser Bot မှ ကြိုဆိုပါတယ်။\n\n"
        "🔑 Key ကျော်ချင်တဲ့ Linkvertise, Link4M သို့မဟုတ် Executor Key Link ကို ပို့ပေးလိုက်ပါဦး။"
    )

async def bypass_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_link = update.message.text
    if "http" not in user_link:
        await update.message.reply_text("❌ ကျေးဇူးပြု၍ Link အမှန်ကို ပို့ပေးပါဗျာ။")
        return

    await update.message.reply_text("⏳ Web Server ကနေ Key ကို လှမ်းယူပေးနေပါပြီ... ခဏစောင့်ပေးပါဗျာ...")
    
    # Ad-link Bypass API ချိတ်ဆက်ခြင်း
    api_url = f"https://api.bypass.vip/bypass?url={user_link}"
    try:
        response = requests.get(api_url)
        data = response.json()
        if data.get("success") == True or "result" in data:
            key_result = data.get("result")
            await update.message.reply_text(f"✅ **Bypass အောင်မြင်ပါတယ်!**\n\n🔑 မင်းရဲ့ Key ကတော့ -\n`{key_result}`\n\n(စာသားကို ဖိပြီး ကူးယူနိုင်ပါတယ်)", parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ စိတ်မကောင်းပါဘူး၊ ဒီ Link ကို ကျော်လို့ မရသေးပါဘူးဗျာ။")
    except:
        await update.message.reply_text("❌ API Server ချိတ်ဆက်မှု Error တက်နေပါတယ်။")

tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bypass_link))

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), tg_app.bot)
        tg_app.update_queue.put(update)
    return "Royald Key Bot Is Running 24/7!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
