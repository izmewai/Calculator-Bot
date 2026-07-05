import re
import asyncio
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

async def welcome_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msgs.pop(update.effective_chat.id, None)
    await update.message.reply_text("ကြိုဆိုစာဖျက်ပြီးပါပြီ ✅")

# 3. Music Bot (Logic)
async def play_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    song_name = " ".join(context.args)
    if not song_name:
        await update.message.reply_text("သီချင်းနာမည်ရိုက်ပေးပါ - /play [song name]")
        return

    wait_msg = await update.message.reply_text("သီချင်းကိုရှာဖွေနေပါတယ် ....")
    await asyncio.sleep(2) 
    
    result_msg = (f"Vc တွင် သီချင်းဖွင့်နေပါပြီ လာရောက်နားဆင်လို့ရပါပြီ ....\n\n"
                  f"သီချင်းနာမယ် - {song_name}\n\n"
                  f"----------- Reven's Music Bot ------------")
    
    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_msg.message_id)
    await update.message.reply_text(result_msg)

    # ၅၀ စက္ကန့် စောင့်ပြီး လူမရှိရင် ထွက်ခြင်း
    await asyncio.sleep(50)
    await update.message.reply_text("' လူလည်းမရှိဘူး... ငါ့တစ်ယောက်တည်းဘဲထားခဲ့ကြတယ် ထွက်ပြီ .... '")

# 4. Admin Tools
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

# 5. Filter & Main Handler
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
    CommandHandler("welcome", set_welcome), CommandHandler("welcomedelete", welcome_delete),
    CommandHandler("play", play_music),
    CommandHandler("ban", ban), CommandHandler("warning", warning),
    CommandHandler("filter", lambda u, c: (filters_data.setdefault(u.effective_chat.id, {}).update({c.args[0]: " ".join(c.args[1:])}), u.message.reply_text("Filter ထည့်သွင်းပြီးပါပြီ ✅"))),
    MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all)
])

print("Bot စတင်ပြီ...")
app.run_polling()
