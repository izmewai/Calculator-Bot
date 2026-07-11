import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Bot Token
TOKEN = "8947711591:AAGblAYzsAL2T0meBSIwT5viF0SD40uZpdU"

# Warning များ သိမ်းဆည်းရန် Dictionary
warnings = {}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Admin ဖြစ်မဖြစ် စစ်ဆေးရန်
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    member = await context.bot.get_chat_member(chat_id, user_id)
    return member.status in ['creator', 'administrator']

# Calculator (2+2 စနစ်)
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        # ဂဏန်းနှင့် သင်္ကေတများကို ရှာပြီး တွက်ချက်ခြင်း
        result = eval(text)
        await update.message.reply_text(f"{text}={result}")
    except:
        pass

# Ban Command
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text("Group မှ ဘန်းလိုက်ပါတယ် ✅")

# Unban Command
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    if context.args:
        user_id = context.args[0]
        await context.bot.unban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text("ဘန်းဖြည်ပြီးပါပြီ ✅")

# Warning System
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

# Welcome Message
welcome_msg = "ဟယ်လိုမဂ်လာပါ"

async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global welcome_msg
    if not await is_admin(update, context): return
    welcome_msg = " ".join(context.args)
    await update.message.reply_text("Welcome စာသားကို ပြောင်းလဲလိုက်ပါပြီ။")

async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(welcome_msg)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("warning", warn))
    app.add_handler(CommandHandler("welcome", set_welcome))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), calculate))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_member))
    
    app.run_polling()
    
