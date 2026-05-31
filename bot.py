import os
import time
import logging
import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# မင်းရဲ့ Telegram Bot Token
BOT_TOKEN = "8952360592:AAG8r9HB4Glihm6h35n4lgNahoxt9GA0L0I"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

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

async def bypass_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_link = update.message.text
    if "http" not in user_link:
        await update.message.reply_text("❌ ကျေးဇူးပြု၍ Link အမှန်ကို ပို့ပေးပါဗျာ။")
        return

    status_msg = await update.message.reply_text("⏳ Premium Web Server ကနေ မင်းရဲ့ Key ကို ကျော်ပေးနေပါပြီ... ခဏစောင့်ပေးပါဗျာ...")
    start_time = time.time()
    
    # Premium Bypass API
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

def main():
    # Telegram Application ကို ရိုးရိုးရှင်းရှင်း တိုက်ရိုက်ဆောက်ပြီး Polling စနစ်နဲ့ Run ခြင်း
    tg_app = Application.builder().token(BOT_TOKEN).build()
    
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bypass_link))
    
    print("🤖 Bot is starting via Polling...")
    tg_app.run_polling()

if __name__ == '__main__':
    main()
