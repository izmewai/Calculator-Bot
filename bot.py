async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in welcome_messages:
        for member in update.message.new_chat_members:
            # User ရဲ့ Name နှင့် ID ကိုယူခြင်း
            user_name = member.first_name
            user_id = member.id
            
            # MarkdownV2 format သုံးပြီး Link ချိတ်ခြင်း
            # [Name](tg://user?id=ID)
            mention_link = f"[{user_name}](tg://user?id={user_id})"
            
            # Message ပို့ခြင်း (parse_mode='MarkdownV2' ကို သေချာထည့်ပေးပါ)
            final_message = f"{mention_link} {welcome_messages[chat_id]}"
            
            await context.bot.send_message(
                chat_id=chat_id, 
                text=final_message, 
                parse_mode='MarkdownV2'
            )
            
