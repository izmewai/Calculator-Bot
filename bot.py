from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import re

# Database တွေအတွက်
welcome_data = {} 
warning_data = {} 
filter_data = {}  

TOKEN = "8971711916:AAHVPZTs_gL0kuUG-9jqYMEeot0wwLkGgNM" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "---- 𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝖡𝖺𝖻𝗒 ----\n\n- ဒီ 𝖡𝗈𝗍 လေးမှာအသုံးပြုနိုင်တာတွေက‌တော့ 𝖢𝖺𝗅𝖼𝗎𝗅𝖺𝗍𝗈𝗋 , 𝖦𝗋𝗈𝗎𝗉 𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝖳𝖾𝗑𝗍 , 𝖥𝗂𝗅𝗍𝖾𝗋 , Ban တို့ဖြစ်ပါတယ် ❤️\n\n- /𝗁𝖾𝗅𝗉 လို့နိုပ်ပြီးတော့ အသုံးပြုပုံတွေကို ကြည့်လို့ရပါတယ် ❤️"
    await update.message.reply_text(msg)

# 1. Calculator
async def calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if re.match(r'^\d+\s*[\+\-\*/]\s*\d+$', text):
        try:
            result = eval(text)
            await update.message.reply_text(f"{text} = {result}")
        except: pass

# 2. Welcome
async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    welcome_text = " ".join(context.args)
    welcome_data[chat_id] = welcome_text
    await update.message.reply_text("ကြိုဆိုစာအသစ်ထည့်သွင်းလိုက်ပါပြီ ✅")

async def del_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in welcome_data:
        del welcome_data[chat_id]
        await update.message.reply_text("ကြိုဆိုစာဖျက်ပြီးပါပြီ , welcome commands သုံးပြီး ကြိုဆိုစာအသစ်ထည့်သွင်းလို့ရပါပြီ ✅")

# 3. Warning
async def warning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.message.reply_to_message.from_user
    user_id = user.id
    if chat_id not in warning_data: warning_data[chat_id] = {}
    warning_data[chat_id][user_id] = warning_data[chat_id].get(user_id, 0) + 1
    count = warning_data[chat_id][user_id]
    if count < 3:
        await update.message.reply_text(f"Warning ( {count} ) ကြိမ်ပေးလိုက်ပါပြီ ၊ 3 ကြိမ်ပြည့်ရင် Group ကနေ Auto Ban ခံရမှာဖြစ်ပါတယ်")
    else:
        await context.bot.ban_chat_member(chat_id, user_id)
        await update.message.reply_text("Warning 3 ကြိမ်ပြည့်ပြီဖြစ်တဲ့အတွက် Group မှ Ban လုပ်ပါတယ်")

# 4. Filter
async def set_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if len(context.args) < 2: return
    keyword, reply = context.args[0], " ".join(context.args[1:])
    if chat_id not in filter_data: filter_data[chat_id] = {}
    filter_data[chat_id][keyword] = reply
    await update.message.reply_text(f"'{keyword}' အတွက် filter ကို ထည့်သွင်းပြီးပါပြီ။")

async def check_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text
    if chat_id in filter_data and text in filter_data[chat_id]:
        await update.message.reply_text(filter_data[chat_id][text])

# 5. Ban
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.reply_to_message.from_user.id
    await context.bot.ban_chat_member(update.effective_chat.id, user_id)
    await update.message.reply_text("Owner Banned From Group")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("welcome", set_welcome))
app.add_handler(CommandHandler("welcomedelete", del_welcome))
app.add_handler(CommandHandler("warning", warning))
app.add_handler(CommandHandler("filter", set_filter))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), calculator))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), check_filter))
if __name__ == '__main__':
    # Web server အတွက် (Render အတွက် လိုအပ်ပါတယ်)
    Thread(target=run_web).start()
    
    # Bot အတွက်
    app.run_webhook(
        listen="0.0.0.0",
        port=8080,
        url_path=TOKEN,
        webhook_url="https://calculator-bot-1-az9k.onrender.com/" + TOKEN)
    
        
