from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# သင့် Bot Token
TOKEN = "8337125844:AAHykBn6tB0ZDJw6peFgYwVWAT29jUXGpSQ"

# 1. Calculator
async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = " ".join(context.args)
        result = eval(user_input)
        await update.message.reply_text(f"{user_input} = {result}")
    except:
        await update.message.reply_text("ဂဏန်းနဲ့ သင်္ကေတပဲ ရိုက်ပေးပါ (ဥပမာ - /calc 10+5)")

# 2. Welcome
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to this Group! 😊")

async def welcome_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝖣𝖾𝗅𝖾𝗍𝖾 𝖣𝗈𝗇𝖾 ✅")

# 3. Warning
warnings = {}
async def warning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Warning ပေးမည့်သူကို Reply ပြန်၍ရိုက်ပါ")
        return
    user_id = update.message.reply_to_message.from_user.id
    warnings[user_id] = warnings.get(user_id, 0) + 1
    if warnings[user_id] == 1:
        await update.message.reply_text("𝖶𝖺𝗋𝗇𝗂𝗇𝗀 𝟣 ကြိမ်ပေးလိုက်ပါပြီ ၊ 𝟥 ကြိမ်ပြည့်ရင် 𝖦𝗋𝗈𝗎𝗉 က 𝖠𝗎𝗍𝗈 𝖡𝖺𝗇𝗇 ခံရမှာဖြစ်ပါတယ်")
    elif warnings[user_id] == 2:
        await update.message.reply_text("𝖶𝖺𝗋𝗇𝗂𝗇𝗀 𝟤 ကြိမ်ရှိနေပါပြီ , 𝟥 ကြိမ်ပြည့်ရင် 𝖦𝗋𝗈𝗎𝗉 ကနေ အပြီးပိုင် 𝖠𝗎𝗍𝗈 𝖡𝖺𝗇𝗇 ခံရမှာပါ")
    else:
        await context.bot.ban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text("Warning 𝟥 ကြိမ်ပြည့်လို့ Group ကနေ အော်တို Bann လုပ်လိုက်ပါပြီနော် 👤")

# 4. MLBB Find
async def find_mlbb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("𝖱𝖾𝗂'𝗌 𝖬𝗅𝖻𝖻 𝖱𝖾𝗀𝗂𝗈𝗇 𝖲𝖾𝖺𝗋𝖼𝗁\n\nName - (အချက်အလက်)\nID - (အိုင်ဒီအမှန်)\nRegion - Myanmar 🇲🇲\n\n---- 𝖱𝖾𝗂'𝗌 ----")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("calc", calc))
    app.add_handler(CommandHandler("welcome", welcome))
    app.add_handler(CommandHandler("welcomedelete", welcome_delete))
    app.add_handler(CommandHandler("warning", warning))
    app.add_handler(CommandHandler("find", find_mlbb))
    print("Bot is running...")
    app.run_polling()
  
