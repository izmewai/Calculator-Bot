from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3

# 1. Database Setup
db = sqlite3.connect("bot.db", check_same_thread=False)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS filters (chat_id INTEGER, word TEXT, response TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS welcome (chat_id INTEGER, text TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS warning (chat_id INTEGER, user_id INTEGER, count INTEGER)")
db.commit()

TOKEN = "8971711916:AAHVPZTs_gL0kuUG-9jqYMEeot0wwLkGgNM"

# 2. Calculator
async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = " ".join(context.args)
        if all(c in "0123456789+-*/. ()" for c in user_input):
            await update.message.reply_text(f"{user_input} = {eval(user_input)}")
    except: pass

# 3. Welcome System
async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    cursor.execute("REPLACE INTO welcome VALUES (?, ?)", (update.effective_chat.id, text))
    db.commit()
    await update.message.reply_text("ကြိုဆိုစာအသစ်ထည့်သွင်းလိုက်ပါပြီ ✅")

async def del_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("DELETE FROM welcome WHERE chat_id=?", (update.effective_chat.id,))
    db.commit()
    await update.message.reply_text("ကြိုဆိုစာဖျက်ပြီးပါပြီ ✅")

# 4. Filter System
async def add_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word, response = context.args[0], " ".join(context.args[1:])
    cursor.execute("INSERT INTO filters VALUES (?, ?, ?)", (update.effective_chat.id, word, response))
    db.commit()
    await update.message.reply_text("Filter ထည့်ပြီးပါပြီ ✅")

# 5. Warning & Ban System
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.reply_to_message.from_user.id
    chat_id = update.effective_chat.id
    cursor.execute("SELECT count FROM warning WHERE chat_id=? AND user_id=?", (chat_id, user_id))
    row = cursor.fetchone()
    count = (row[0] + 1) if row else 1
    
    if count >= 3:
        await context.bot.ban_chat_member(chat_id, user_id)
        await update.message.reply_text("Warning 3 ကြိမ်ပြည့်ပြီဖြစ်တဲ့အတွက် Group မှ Ban လုပ်ပါတယ်")
    else:
        cursor.execute("REPLACE INTO warning VALUES (?, ?, ?)", (chat_id, user_id, count))
        db.commit()
        await update.message.reply_text(f"Warning ({count}) ကြိမ်ပေးလိုက်ပါပြီ ၊ 3 ကြိမ်ပြည့်ရင် Group ကနေ Auto Ban ခံရမှာဖြစ်ပါတယ်")

# 6. Start & Help
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("---- 𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝖡𝖺𝖻𝗒 ----\n- 𝖢𝖺𝗅𝖼𝗎𝗅𝖺𝗍𝗈𝗋 , 𝖶𝖾𝗅𝖼𝗈𝗆𝖾 , 𝖥𝗂𝗅𝗍𝖾𝗋 , Ban တို့ဖြစ်ပါတယ် ❤️\n- /𝗁𝖾𝗅𝗉 လို့နိုပ်ပြီး အသုံးပြုပုံတွေကို ကြည့်လို့ရပါတယ် ❤️")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("calc", calc))
    app.add_handler(CommandHandler("welcome", set_welcome))
    app.add_handler(CommandHandler("welcomedelete", del_welcome))
    app.add_handler(CommandHandler("filter", add_filter))
    app.add_handler(CommandHandler("warning", warn))
    print("Bot is running...")
    app.run_polling()
