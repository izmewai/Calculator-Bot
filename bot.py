import re
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

# 2. MLBB Region Check (Mockup System - API မလိုဘဲ စမ်းသပ်ရန်)
async def check_mlbb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    numbers = re.findall(r'\d+', update.message.text)
    if len(numbers) < 2:
        await update.message.reply_text("အမှား - /check [ID] [Server] ဟု ရိုက်ပေးပါ။")
        return
    
    user_id = numbers[0]
    server_id = numbers[1]
    
    # ရှာဖွေနေကြောင်း ပြသခြင်း
    wait_msg = await update.message.reply_text("Mlbb Account ကိုရှာဖွေနေပါတယ် ....")
    
    # ဤနေရာတွင် ID ကိုစစ်ဆေးသည် (ဥပမာ - 123456789 ဆိုရင် တွေ့တယ်လို့ သတ်မှတ်သည်)
    if user_id == "123456789":
        name = "Reven"
        region = "Myanmar"
        result_msg = (f"----- Reven's Mlbb Region Check -----\n\n"
                      f"Account Name - {name}\n"
                      f"Id - {user_id} ({server_id})\n"
                      f"Region - {region}\n\n"
                      f"-------------------------------------------------------")
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_msg.message_id)
        await update.message.reply_text(result_msg)
    else:
        # မတွေ့ပါက ပြမည့်စာ
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_msg.message_id)
        await update.message.reply_text("ID + SEVER ကိုရှာမတွေ့ပါ ။ သေချာစွာစစ်ဆေးပြီးပြန်ပို့ပါ ။")

# 3. အခြား Features များ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("---- 𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝖡𝖺𝖻𝗒 ----\n\n- /help ဖြင့်ကြည့်နိုင်ပါတယ် ❤️")

async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msgs[update.effective_chat.id] = " ".join(context.args)
    await update.message.reply_text("ကြိုဆိုစာအသစ်ထည့်သွင်းလိုက်ပါပြီ ✅")

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

# Handlers Setup
app = ApplicationBuilder().token(TOKEN).build()
app.add_handlers([
    CommandHandler("start", start),
    CommandHandler("check", check_mlbb),
    CommandHandler("welcome", set_welcome),
    CommandHandler("ban", ban),
    CommandHandler("warning", warning),
    MessageHandler(filters.TEXT & (~filters.COMMAND), lambda u, c: calc(u, c) if not filters_data.get(u.effective_chat.id, {}).get(u.message.text) else u.message.reply_text(filters_data[u.effective_chat.id][u.message.text]))
])

print("Bot စတင်ပြီ...")
app.run_polling()
