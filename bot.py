import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from flask import Flask
from threading import Thread

# --- Flask Server ---
app_web = Flask(__name__)
@app_web.route('/')
def home():
    return "Bot is running!"

def run_web():
    app_web.run(host='0.0.0.0', port=8080)

# --- Configuration ---
TOKEN = "YOUR_TOKEN_HERE" 
OWNER_ID = 8454178636 # သင့်ရဲ့ ID အမှန်

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

warnings = {}
welcome_messages = {}

# --- Admin Check ---
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        if member.status in ['creator', 'administrator']:
            return True
        else:
            await update.message.reply_text("အုံနာနဲ့အက်မင်တွေသာဒီအရာတွေကိုအသုံးပြုနိုင်ပါတယ် ။")
            return False
    except:
        return False

# --- Scammer Report (/scm) ---
async def report_scammer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Scammer လို့ထင်တဲ့သူရဲ့ စာကို Reply ပြန်ပြီး /scm လို့ ပို့ပေးပါ။")
        return

    reported_user = update.message.reply_to_message.from_user
    reporter_user = update.effective_user
    chat = update.effective_chat

    await update.message.reply_text("Scammer ဟုတိုင်ကြားထားပါသည် ၊ အချက်အလတ်များကိုစစ်ဆေးနေပါသည် ....")

    report_text = (
        f"--- တိုင်ကြားမှုအသစ် ---\n\n"
        f"Scammer ဟုတိုင်ကြားခံရသူ - @{reported_user.username or reported_user.id}\n"
        f"တိုင်ကြားသူ - @{reporter_user.username or reporter_user.id}\n"
        f"တိုင်ကြားထားသော Gp - {chat.title}\n"
        f"-------------------------------------------------------"
    )
    await context.bot.send_message(chat_id=OWNER_ID, text=report_text)

# --- Features ---
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if any(op in text for op in ['+', '-', '*', '/']):
        try:
            result = eval(text)
            await update.message.reply_text(f"📊 {text} = {result}")
        except: pass

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
        await update.message.reply_text(f"🚫 {user.first_name} ကို Group မှ ဘန်းလိုက်ပါပြီ။")

async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        warnings[user.id] = warnings.get(user.id, 0) + 1
        if warnings[user.id] >= 3:
            await context.bot.ban_chat_member(update.effective_chat.id, user.id)
            await update.message.reply_text(f"🚫 {user.first_name} သည် သတိပေးချက် ၃ ကြိမ်ပြည့်၍ ဘန်းလိုက်ပါပြီ။")
            warnings[user.id] = 0
        else:
            await update.message.reply_text(f"⚠️ {user.first_name} သတိပေးချက် {warnings[user.id]} ကြိမ်မြောက်။")

async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    msg = " ".join(context.args)
    if msg:
        welcome_messages[update.effective_chat.id] = msg
        await update.message.reply_text("✅ ကြိုဆိုစာကို သိမ်းဆည်းလိုက်ပါပြီ။")

async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in welcome_messages:
        for member in update.message.new_chat_members:
            text = f'👋 <a href="tg://user?id={member.id}">{member.first_name}</a> {welcome_messages[chat_id]}'
            await context.bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')

# --- Main App ---
if __name__ == '__main__':
    Thread(target=run_web).start() 
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("scm", report_scammer))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("warning", warn))
    app.add_handler(CommandHandler("welcome", set_welcome))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), calculate))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_member))
    
    app.run_polling()
    
