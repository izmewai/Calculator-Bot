from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# သင့် Bot Token နှင့် Admin ID
TOKEN = "8686667809:AAESji8x0LLe9v0bU3H-buExwoiYe6Nz58A"
ADMIN_ID = 8454178636

def start(update: Update, context: CallbackContext):
    text = (
        "𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝖥𝗋𝗈𝗆 𝖡𝖾𝗋𝗋𝗒'𝗌 𝖲𝗁𝗈𝗉 \n\n"
        "ဒီ 𝖡𝗈𝗍 လေးမှာ 𝗂𝗍𝖾𝗆𝗌 အစုံတော်တော်များများကိုဝယ်ယူနိုင်ပါတယ် \n\n"
        "အမြန်ဆန်ဆုံး 𝖥𝖺𝗌𝗍𝖾𝗌𝗍 𝖲𝖾𝗋𝗏𝗂𝖼𝖾 ပေးမှာမို့ ယုံကြည်စိတ်ချလို့ရပါတယ်  \n\n"
        "ရရှိနိုင်တာတွေကတော့ 𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 , 𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝖲𝗍𝖺𝗋 , 𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝖠𝖼𝖼𝗈𝗎𝗇𝗍 ဖြစ်ပြီး ကိုယ်ဝယ်ယူချင်တဲ့အရာတွေကိုလည်းမေးဝယ်လို့ရပါတယ် \n\n"
        "𝖭𝖿𝗍 တွေလည်းရနိုင်တာတွေကို 𝖴𝗉𝖽𝖺𝗍𝖾 နေ့စဉ် 𝖡𝗈𝗍 ဘက်ကပေးနေမှာပါ \n\n"
        "𝖳𝗒𝗌𝗆 𝖥𝗈𝗋 𝗎𝗌𝗂𝗇𝗀 𝗆𝗒 𝖻𝗈𝗍 𝖦𝗎𝗒𝗌𝗌 ... "
    )
    keyboard = [
        [InlineKeyboardButton("🛒 ရရှိနိုင်သည်များ", callback_data='price_list')],
        [InlineKeyboardButton("💳 Buy", callback_data='buy_process')],
        [InlineKeyboardButton("📩 စာပို့မည်", callback_data='contact_admin')]
    ]
    update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == 'price_list':
        text = (
            "𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖯𝗋𝗂𝖼𝖾 \n\n"
            "𝟣𝗆𝗈𝗇𝗍𝗁 - 𝟤𝟥𝟧𝟢𝟢𝖪𝗌 (Login ပေးဝင်ရပါမယ်)\n"
            "𝟥𝗆𝗈𝗇𝗍𝗁 - 𝟧𝟨𝟧𝟢𝟢𝖪𝗌 | 𝟨𝗆𝗈𝗇𝗍𝗁 - 𝟩𝟧𝟧𝟢𝟢𝖪𝗌 | 𝟣𝗒𝖾𝖺𝗋 - 𝟣𝟤𝟪𝟧𝟢𝟢𝖪𝗌 (Gift Plan)\n\n"
            "𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝖲𝗍𝖺𝗋 𝖯𝗋𝗂𝖼𝖾 \n"
            "𝟧𝟢-𝟥𝟩𝟢𝟢 | 𝟩𝟧-𝟨𝟥𝟢𝟢 | 𝟣𝟢𝟢-𝟩𝟣𝟢𝟢 | 𝟣𝟧𝟢-𝟣𝟦𝟢𝟢𝟢 | 𝟤𝟢𝟢-𝟣𝟨𝟧𝟢𝟢 | 𝟥𝟢𝟢-𝟤𝟦𝟧𝟢𝟢 | 𝟦𝟢𝟢-𝟥𝟦𝟢𝟢𝟢 | 𝟧𝟢𝟢-𝟥𝟪𝟧𝟢𝟢 | 𝟣𝟢𝟢𝟢-𝟩𝟨𝟧𝟢𝟢\n\n"
            "𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝖠𝖼𝖼𝗈𝗎𝗇𝗍 𝖯𝗋𝗂𝖼𝖾 \n"
            "𝟣 𝖠𝖼𝖼 𝟣𝟦𝟢𝟢𝖪𝗌 (Myanmar Phone Number)"
        )
        query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data='start')]]))
    
    elif query.data == 'buy_process':
        query.edit_message_text("Payment Wave - 09428232096 NK \n( Bill လက်မခံ မိနစ် ၃၀ ကျော်သောပြေစာလက်မခံ မှားလွှဲတာဝန်မယူ ) \n\nပြေစာပုံကို ဒီ Bot ဆီ ပုံအနေနဲ့ ပို့ပေးပါ။")
    
    elif query.data == 'contact_admin':
        query.edit_message_text("အဆင်မပြေသည်များရှိပါက >> @cuzmei ကိုလာပါ ။")
    
    elif query.data == 'start':
        start(update, context)

    elif query.data.startswith('accept_'):
        if update.effective_user.id == ADMIN_ID:
            user_id = query.data.split('_')[1]
            context.bot.send_message(chat_id=user_id, text="သင်၏အော်ဒါတင်မှုအောင်မြင်ပါသည် ✅ ၊ စောင့်ဆိုင်းပါ ...")
            query.edit_message_text("အော်ဒါလက်ခံလိုက်ပါပြီ။")
    
    elif query.data.startswith('reject_'):
        if update.effective_user.id == ADMIN_ID:
            user_
          
