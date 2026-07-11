import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TOKEN = "8947711591:AAGblAYzsAL2T0meBSIwT5viF0SD40uZpdU"
warnings = {}
# Welcome message ကို သိမ်းထားရန် Dictionary
welcome_messages = {}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    member = await context.bot.get_chat_member(chat_id, user_id)
    return member.status in ['creator', 'administrator']

# Welcome Command
async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    chat_id = update.effective_chat.id
    msg = " ".join(context.args)
    if msg:
        welcome_messages[chat_id] = msg
        await update.message.reply_text("သင်၏ ကြိုဆိုစာကို ထည့်သွင်းလိုက်ပါပြီ ✅")
    else:
        await update.message.reply_text("ကျေးဇူးပြု၍ ကြိုဆိုစာထည့်ပေးပါ (ဥပမာ: /welcome hello)")

# Welcome Delete Command
async def delete_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    chat_id = update.effective_chat.id
    if chat_id in welcome_messages:
        del welcome_messages[chat_id]
        await update.message.reply_text("ကြိုဆိုစာ‌အဟောင်းဖျက်ပြီးပါပြီ ၊ ကြိုဆိုစာအသစ်ထည့်လို့ရပါပြီ ✅")

# New Member Handler
async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in welcome_messages:
        for member in update.message.new_chat_members:
            # User Name ကို ယူခြင်း
            user_name = member.first_name
            # အသုံးပြုသူတောင်းဆိုထားသည့် ပုံစံ (Name + Message)
            final_message = f"{user_name} {welcome_messages[chat_id]}"
            await context.bot.send_message(chat_id=chat_id, text=final_message)

# (ယခင် Ban, Unban, Warning, Calculator တို့ကိုလည်း ဆက်လက်အသုံးပြုနိုင်သည်)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("welcome", set_welcome))
    app.add_handler(CommandHandler("welcomedelete", delete_welcome))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_member))
    
    # ... အခြား handler များထည့်ပါ ...
    
    app.run_polling()
