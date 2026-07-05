from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import re

# 1. Configuration & Data Storage
TOKEN = "8971711916:AAHVPZTs_gL0kuUG-9jqYMEeot0wwLkGgNM"

# Dictionary များကို Group ID အလိုက် သိမ်းဆည်းရန်
welcome_msgs = {} # {chat_id: text}
filters_data = {} # {chat_id: {keyword: reply}}
warnings = {}     # {chat_id: {user_id: count}}

# 2. Start & Help
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = ("---- 𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝖡𝖺𝖻𝗒 ----\n\n"
           "- ဒီ 𝖡𝗈𝗍 လေးမှာအသုံးပြုနိုင်တာတွေက‌တော့ 𝖢𝖺𝗅𝖼𝗎𝗅𝖺𝗍𝗈𝗋 , 𝖦𝗋𝗈𝗎𝗉 𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝖳𝖾𝗑𝗍 , 𝖥𝗂𝗅𝗍𝖾𝗋 , Ban တို့ဖြစ်ပါတယ် ❤️\n\n"
           "- /𝗁𝖾𝗅𝗉 လို့နိုပ်ပြီးတော့ အသုံးပြုပုံတွေကို ကြည့်လို့ရပါတယ် ❤️")
    await update.message.reply_text(msg)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = ("𝖧𝗈𝗐 𝗍𝗈 𝗎𝗌𝖾 𝗆𝗒 𝖻𝗈𝗍\n\n• Calculator\n- 1+1, 2*2 စသဖြင့် တွက်ချက်နိုင်ပါသည်။\n\n"
           "• Group Welcome\n- /welcome [စာသား] (Welcome စာသတ်မှတ်ရန်)\n- /welcomedelete (ဖျက်ရန်)\n\n"
           "• /filter\n- /filter [Keyword] [Reply] (ဥပမာ - /filter Kpay 09xxx)\n\n"
           "• Ban / Unban\n- စာထောက်ပြီး /ban , /unban\n\n"
           "• Warning\n- စာထောက်ပြီး /warning (3 ကြိမ်ပြည့်ရင် Auto Ban)")
    await update.message.reply_text(msg)

# 3. Calculator
async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if re.match(r'^\d+\s*[\+\-\*/]\s*\d+$', text):
        try:
            result = eval(text)
            await update.message.reply_text(f"{text} = {result}")
        except: pass

# 4. Welcome System
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in welcome_msgs:
        await update.message.reply_text(welcome_msgs[chat_id])

async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msgs[update.effective_chat.id] = " ".join(context.args)
    await update.message.reply_text("ကြိုဆိုစာအသစ်ထည့်သွင်းလိုက်ပါပြီ ✅")

async def welcome_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msgs.pop(update.effective_chat.id, None)
    await update.message.reply_text("ကြိုဆိုစာဖျက်ပြီးပါပြီ , welcome commands သုံးပြီး ကြိုဆိုစာအသစ်ထည့်သွင်းလို့ရပါပြီ ✅")

# 5. Admin (Ban/Unban/Warning)
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text("Owner Banned From Group")

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.unban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text("User ကို ပြန်လည်ဖြည်ပေးလိုက်ပါပြီ။")

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

# 6. Filter System
async def set_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if len(context.args) < 2: return
    if chat_id not in filters_data: filters_data[chat_id] = {}
    filters_data[chat_id][context.args[0]] = " ".join(context.args[1:])
    await update.message.reply_text(f"'{context.args[0]}' အတွက် filter ကို ထည့်သွင်းပြီးပါပြီ။")

async def check_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.effective_chat.id
    if chat_id in filters_data and text in filters_data[chat_id]:
        await update.message.reply_text(filters_data[chat_id][text])
    else:
        await calc(update, context)

# 7. Main App
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("welcome", set_welcome))
app.add_handler(CommandHandler("welcomedelete", welcome_delete))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("unban", unban))
app.add_handler(CommandHandler("warning", warning))
app.add_handler(CommandHandler("filter", set_filter))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), check_filter))

print("Bot စတင်နေပြီ...")
app.run_polling()
