import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8971711916:AAHVPZTs_gL0kuUG-9jqYMEeot0wwLkGgNM"

welcome_msgs, filters_data, warnings = {}, {}, {}

# 1. Calculator
async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if re.match(r'^\d+\s*[\+\-\*/]\s*\d+$', text):
        try:
            res = eval(text)
            await update.message.reply_text(f"{text} = {res}")
        except: pass

# 2. MLBB Region Check (API နည်းလမ်း)
async def check_mlbb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    numbers = re.findall(r'\d+', update.message.text)
    if len(numbers) < 2:
        await update.message.reply_text("အမှား - /check [ID] [Server] ဟု ရိုက်ပေးပါ။")
        return
    
    user_id, server_id = numbers[0], numbers[1]
    wait_msg = await update.message.reply_text("Mlbb Account ကိုရှာဖွေနေပါတယ် ....")
    
    # [အရေးကြီး] ဤနေရာတွင် သင်ရရှိထားသော API Link ကို အစားထိုးပါ
    api_url = f"https://api.vapi.xyz/mlbb/info?id={user_id}&zone={server_id}"
    
    try:
        response = requests.get(api_url, timeout=10).json()
        if response.get("status") == "success":
            result_msg = (f"----- Reven's Mlbb Region Check -----\n\n"
                          f"Account Name - {response.get('name')}\n"
                          f"Id - {user_id} ({server_id})\n"
                          f"Region - {response.get('region')}\n\n"
                          f"-------------------------------------------------------")
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_msg.message_id)
            await update.message.reply_text(result_msg)
        else:
            raise Exception()
    except:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_msg.message_id)
        await update.message.reply_text("ID + SEVER ကိုရှာမတွေ့ပါ ။ သေချာစွာစစ်ဆေးပြီးပြန်ပို့ပါ ။")

# 3. Admin & Welcome
async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msgs[update.effective_chat.id] = " ".join(context.args)
    await update.message.reply_text("ကြိုဆိုစာအသစ်ထည့်သွင်းလိုက်ပါပြီ ✅")

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

# 4. Filter Handler
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
    CommandHandler("check", check_mlbb),
    CommandHandler("welcome", set_welcome),
    CommandHandler("ban", ban),
    CommandHandler("warning", warning),
    CommandHandler("filter", lambda u, c: (filters_data.setdefault(u.effective_chat.id, {}).update({c.args[0]: " ".join(c.args[1:])}), u.message.reply_text("Filter ထည့်သွင်းပြီးပါပြီ ✅"))),
    MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all)
])

print("Bot စတင်ပြီ...")
app.run_polling()
