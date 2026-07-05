import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import re

TOKEN = "8971711916:AAHVPZTs_gL0kuUG-9jqYMEeot0wwLkGgNM"

# Data Storage
welcome_msgs, filters_data, warnings = {}, {}, {}

# 1. Calculator (ရှင်းလင်းစွာ)
async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if re.match(r'^\d+\s*[\+\-\*/]\s*\d+$', text):
        try:
            result = eval(text)
            await update.message.reply_text(f"{text} = {result}")
        except: pass

# 2. MLBB Check (ID နှင့် Server ခွဲခြားခြင်း)
async def check_mlbb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # အသုံးပြုသူပို့လိုက်တဲ့ စာထဲက ဂဏန်းတွေကို အကုန်ထုတ်ယူ (ID နှင့် Server ခွဲရန်)
    numbers = re.findall(r'\d+', update.message.text)
    
    if len(numbers) < 2:
        await update.message.reply_text("အမှား - /check [ID] [Server] ဟု ရိုက်ပေးပါ။")
        return
    
    user_id = numbers[0]
    server_id = numbers[1]
    
    await update.message.reply_text("🔎 ရှာဖွေနေပါသည်...")
    
    # ဤနေရာတွင် သင်သုံးမည့် MLBB API ကို အစားထိုးပါ
    # ဥပမာ - API URL တစ်ခုကို request လုပ်ခြင်း
    # response = requests.get(f"https://api.example.com/check?id={user_id}&zone={server_id}")
    
    msg = (f"------ Reven Mlbb Check -----\n\n"
           f"Account Name - (APIမှရရှိသောနာမည်)\n"
           f"Id - {user_id} ({server_id})\n"
           f"Region - (APIမှရရှိသောဒေသ)\n\n"
           f"-------------------------------------------------------")
    await update.message.reply_text(msg)

# 3. Features (Welcome, Ban, Warning, Filter) - ယခင်အတိုင်း
async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msgs[update.effective_chat.id] = " ".join(context.args)
    await update.message.reply_text("ကြိုဆိုစာအသစ်ထည့်သွင်းလိုက်ပါပြီ ✅")

async def welcome_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msgs.pop(update.effective_chat.id, None)
    await update.message.reply_text("ကြိုဆိုစာဖျက်ပြီးပါပြီ ✅")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text("Owner Banned From Group")

async def warning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.message.reply_to_message.from_user.id
    if chat_id not in warnings: warnings[chat_id] = {}
    warnings[chat_id][user_id] = warnings[chat_id].get(user_id, 0) + 1
    count = warnings[chat_id][user_id]
    if count >= 3:
        await context.bot.ban_chat_member(chat_id, user_id)
        await update.message.reply_text("Warning 3 ကြိမ်ပြည့်ပြီဖြစ်တဲ့အတွက် Group မှ Ban လုပ်ပါတယ်")
    else:
        await update.message.reply_text(f"Warning ( {count} ) ကြိမ်ပေးလိုက်ပါပြီ ၊ 3 ကြိမ်ပြည့်ရင် Group ကနေ Auto Ban ခံရမှာဖြစ်ပါတယ်")

async def check_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.effective_chat.id
    if chat_id in filters_data and text in filters_data[chat_id]:
        await update.message.reply_text(filters_data[chat_id][text])
    else:
        await calc(update, context)

# App Setup
app = ApplicationBuilder().token(TOKEN).build()
app.add_handlers([
    CommandHandler("start", lambda u, c: u.message.reply_text("Reven Bot စတင်နေပါပြီ!")),
    CommandHandler("check", check_mlbb),
    CommandHandler("welcome", set_welcome), CommandHandler("welcomedelete", welcome_delete),
    CommandHandler("ban", ban), CommandHandler("warning", warning),
    CommandHandler("filter", set_filter),
    MessageHandler(filters.TEXT & (~filters.COMMAND), check_filter)
])

app.run_polling()
