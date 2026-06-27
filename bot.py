from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import re

async def calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # ဂဏန်းတွေ၊ +, -, *, / သင်္ကေတတွေပဲ ပါတဲ့စာကိုမှ တွက်ခိုင်းမယ်
    # ဒီကုဒ်က ရိုးရိုး ဂဏန်းအလုံးကြီး (ဥပမာ 1000) တွေကိုတော့ တွက်ချက်မှာ မဟုတ်ပါဘူး
    if re.match(r'^[\d\+\-\*\/\.\(\)\s]+$', user_text):
        try:
            result = eval(user_text)
            await update.message.reply_text(f"{user_text} = {result}")
        except:
            pass 
    else:
        # ဂဏန်းအပြင် တခြားစာလုံးတွေပါရင် Bot က ဘာမှပြန်မပြောဘဲ တိတ်ဆိတ်နေပါမယ်
        pass

if __name__ == '__main__':
    app = ApplicationBuilder().token("8678628379:AAFgyXDmEMjy2D91wSR4Iu8B1Bma_OspOj4").build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), calculator))
    app.run_polling()
