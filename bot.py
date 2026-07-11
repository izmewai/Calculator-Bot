import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TOKEN = "8947711591:AAGblAYzsAL2T0meBSIwT5viF0SD40uZpdU"

warnings = {}
welcome_messages = {}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Admin ဖြစ်မဖြစ် စစ်ဆေးရန် (Commands အားလုံးအတွက်)
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        return member.status in ['creator', 'administrator']
    except:
        return False

# Calculator (Admin မလိုပါ)
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        if "+" in text or "-" in text or "*" in text or "/" in text:
            result = eval(text)
            await update.message.reply_text(f"{text} = {result}")
    except:
        pass

# Ban Command (Admin Only)
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): 
        await update.message.reply_text("Admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text("Group မှ ဘန်းလိုက်ပါတယ် ✅")

# Unban Command (Admin Only)
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    if context.args:
        user_id = context.args[0]
        await context.bot.unban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text("ဘန်းဖြည်ပြီးပါပြီ ✅")

# Warning Command (Admin Only)
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        warnings[user_id] = warnings.get(user_id, 0) + 1
        
        if warnings[user_id] == 1:
            await update.message.reply_text("သင့်ကို Warning 1 ကြိမ်ပေးလိုက်ပြီ ✅ 3 ကြိမ်ပြည့်ပါက Group မှ Auto Ban ခံရမှာဖြစ်ပါတယ်")
        elif warnings[user_id] == 2:
            await update.message.reply_text("သင်၏ Warning 2 ကြိမ်ရှိသွားပါပြီ , 3 ကြိမ်ပြည့်လျှင် Group မှ Auto Ban ခံရမှာဖြစ်ပါတယ် ✅")
        elif warnings[user_id] >= 3:
            await context.bot.ban_chat_member(update.effective_chat.id, user_id)
            await update.message.reply_text("ဝမ်းနည်းပါတယ် , Warning 3 ကြိမ်ပြည့်ပြီဖြစ်တဲ့အတွက် Group မှ Banned လုပ်လိုက်ပါသည် 🚫")
            warnings[user_id] = 0

# Welcome Setup (Admin Only)
async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    chat_id = update.effective_chat.id
    msg = " ".join(context.args)
    if msg:
        welcome_messages[chat_id] = msg
        await update.message.reply_text("သင်၏ ကြိုဆိုစာကို ထည့်သွင်းလိုက်ပါပြီ ✅")
    else:
        await update.message.reply_text("ကျေးဇူးပြု၍ ကြိုဆိုစာထည့်ပေးပါ (ဥပမာ: /welcome hello)")

# Welcome Delete (Admin Only)
async def delete_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    chat_id = update.effective_chat.id
    if chat_id in welcome_messages:
        del welcome_messages[chat_id]
        await update.message.reply_text("ကြိုဆိုစာ‌အဟောင်းဖျက်ပြီးပါပြီ ၊ ကြိုဆိုစာအသစ်ထည့်လို့ရပါပြီ ✅")

# New Member Greet (HTML Format)
async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in welcome_messages:
        for member in update.message.new_chat_members:
            user_name = member.first_name
            user_id = member.id
            mention_link = f'<a href="tg://user?id={user_id}">{user_name}</a>'
            await context.bot.send_message(
                chat_id=chat_id, 
                text=f"{mention_link} {welcome_messages[chat_id]}", 
                parse_mode='HTML'
            )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("warning", warn))
    app.add_handler(CommandHandler("welcome", set_welcome))
    app.add_handler(CommandHandler("welcomedelete", delete_welcome))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), calculate))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_member))
    
    app.run_polling()
    
