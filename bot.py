import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8971711916:AAHVPZTs_gL0kuUG-9jqYMEeot0wwLkGgNM"

# Data Storage
welcome_msgs, filters_data, warnings = {}, {}, {}

# 1. Calculator
async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if re.match(r'^\d+\s*[\+\-\*/]\s*\d+$', text):
        try:
            res = eval(text)
            await update.message.reply_text(f"{text} = {res}")
        except: pass

# 2. Welcome System
async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msgs[update.effective_chat.id] = " ".join(context.args)
    await update.message.reply_text("ကြိုဆိုစာအသစ်ထည့်သွင်းလိုက်ပါပြီ ✅")

# 3. Admin Tools
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        await context.bot.ban_chat_member(update.effective_chat.id, update.message.reply_to_message.from_user.id)
        await update.message.reply_text("Owner Banned From Group")

async def warning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id, user_id = update.effective_chat.id, update.message.reply_to_message.from_user.id
    if chat_id not in warnings: warnings[chat_id] = {}
    warnings[chat_id][user_id] = warnings[chat_id].get(user_id, 0) + 1
    if warnings[chat_id][user_id] >= 3:
        await context.bot.ban_chat_member(chat_id, user_id)
        await update.message.reply_text("Warning 3 ကြိမ်ပြည့်၍ Group မှ Ban လုပ်လိုက်ပါပြီ။")
    else:
        await update.message.reply_text(f"Warning ({warnings[chat_id][user_id]}) ကြိမ်ပေးလိုက်ပါပြီ။")

# 4. Filter System
async def set_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2: return
    key = context.args[0]
    value = " ".join(context.args[1:])
    chat_id = update.effective_chat.id
    if chat_id not in filters_data: filters_data[chat_id] = {}
    filters_data[chat_id][key] = value
    await update.message.reply_text(f"'{key}' အတွက် filter ကို ထည့်သွင်းပြီးပါပြီ ✅")

# 5. Handler
async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text
    if chat_id in filters_data and text in filters_data[chat_id]:
        await update.message.reply_text(filters_data[chat_id][text])
    else:
        await calc(update, context)

# App Setup
app = ApplicationBuilder().token(TOKEN).build()
app.add_handlers([
    CommandHandler("start", lambda u, c: u.message.reply_text("Reven Bot စတင်နေပါပြီ!")),
    CommandHandler("welcome", set_welcome),
    CommandHandler("ban", ban),
    CommandHandler("warning", warning),
    CommandHandler("filter", set_filter),
    MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all)
])

print("Bot စတင်ပြီ...")
app.run_polling()
