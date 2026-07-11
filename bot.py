import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TOKEN = "8947711591:AAGblAYzsAL2T0meBSIwT5viF0SD40uZpdU"

# ဒေတာသိမ်းရန် Dictionary များ
warnings = {}
welcome_messages = {}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- Admin စစ်ဆေးရန် Function ---
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        return member.status in ['creator', 'administrator']
    except:
        return False

# --- Calculator ---
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if any(op in text for op in ['+', '-', '*', '/']):
        try:
            result = eval(text)
            await update.message.reply_text(f"{text} = {result}")
        except:
            pass

# --- Ban / Unban ---
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
        await update.message.reply_text(f"{user.first_name} ကို Group မှ ဘန်းလိုက်ပါတယ် ✅")

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    if context.args:
        user_id = context.args[0]
        await context.bot.unban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text("ဘန်းဖြည်ပြီးပါပြီ ✅")

# --- Warning System ---
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        warnings[user.id] = warnings.get(user.id, 0) + 1
        
        if warnings[user.id] >= 3:
            await context.bot.ban_chat_member(update.effective_chat.id, user.id)
            await update.message.reply_text(f"ဝမ်းနည်းပါတယ် {user.first_name}, Warning 3 ကြိမ်ပြည့်ပြီဖြစ်တဲ့အတွက် Group မှ Banned လုပ်လိုက်ပါသည် 🚫")
            warnings[user.id] = 0
        else:
            await update.message.reply_text(f"သတိပေးချက် {warnings[user.id]} ကြိမ်မြောက်! 3 ကြိမ်ပြည့်ပါက Auto Ban ခံရမည်။")

# --- Welcome System ---
async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    msg = " ".join(context.args)
    if msg:
        welcome_messages[update.effective_chat.id] = msg
        await update.message.reply_text("သင်၏ ကြိုဆိုစာကို ထည့်သွင်းလိုက်ပါပြီ ✅")
    else:
        await update.message.reply_text("အသုံးပြုပုံ: /welcome [စာသား]")

async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in welcome_messages:
        for member in update.message.new_chat_members:
            text = f'<a href="tg://user?id={member.id}">{member.first_name}</a> {welcome_messages[chat_id]}'
            await context.bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')

# --- Main App ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("warning", warn))
    app.add_handler(CommandHandler("welcome", set_welcome))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), calculate))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_member))
    
    print("Bot စတင်လည်ပတ်နေပါပြီ...")
    app.run_polling()
    
