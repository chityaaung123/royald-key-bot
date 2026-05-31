import os
import time
import logging
import requests
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)

# မင်းရဲ့ Telegram Bot Token 
BOT_TOKEN = "8952360592:AAG8r9HB4Glihm6h35n4lgNahoxt9GA0L0I"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
tg_app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🤖 **Royald Hub Premium Bypasser မှ ကြိုဆိုပါတယ်!**\n\n"
        "🔗 Platoboost, Delta, Hydrogen, Linkvertise စတဲ့ "
        "ထောက်ပံ့ထားတဲ့ Link အမျိုးအစားပေါင်း ၄၂ ခုကျော်ကို အခမဲ့ ကျော်ပေးနိုင်ပါပြီဗျာ။\n\n"
        "👉 စမ်းသပ်ဖို့ မင်းရဲ့ Key Link ကို ပို့ပေးလိုက်ပါဦး!",
        parse_mode='Markdown'
    )

async def bypass_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_link = update.message.text
    if "http" not in user_link:
        await update.message.reply_text("❌ ကျေးဇူးပြု၍ Link အမှန်ကို ပို့ပေးပါဗျာ။")
        return

    status_msg = await update.message.reply_text("⏳ Premium Web Server ကနေ မင်းရဲ့ Key ကို ကျော်ပေးနေပါပြီ... ခဏစောင့်ပေးပါဗျာ...")
    
    # စက္ကန့်တွက်ချက်ရန် စတင်ချိန်ကို မှတ်သားခြင်း
    start_time = time.time()
    
    # ကမ္ဘာလုံးဆိုင်ရာ အားကောင်းသော Premium Bypass API 
    api_url = f"https://api.freebypasser.xyz/api/bypass?url={user_link}"
    
    try:
        response = requests.get(api_url, timeout=40)
        data = response.json()
        
        # အချိန်ဘယ်လောက်ကြာသွားလဲ တွက်ချက်ခြင်း
        time_taken = round(time.time() - start_time, 2)
        
        # API Response ထဲက ဒေတာတွေကို စစ်ဆေးခြင်း
        success = data.get("success", False)
        key_result = data.get("result") or data.get("key") or data.get("bypassed")
        link_type = data.get("type", "Bypass")

        if success and key_result:
            # မင်းပြထားတဲ့ ပုံစံအတိုင်း ကွက်တိ Format ပြန်ထုတ်ပေးခြင်း
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

tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bypass_link))

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), tg_app.bot)
        tg_app.update_queue.put(update)
    return "Premium Key Bot Is Running 24/7!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
