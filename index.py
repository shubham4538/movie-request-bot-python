import tracemalloc
tracemalloc.start()

# from telegram import Update
from telegram.constants import ChatMemberStatus
from telegram.ext import *
from telegram.ext import filters, ApplicationBuilder
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')
database_url = os.environ.get('DATABASE_URL')
print(API_TOKEN, database_url)

API_TOKEN = '8154517633:AAFKou25tAAl-0FlUKe4tw-K-MFhw4zFciA'
print('Starting a bot...')

async def start_commmand(update, context):
  await update.message.reply_text("Hello! You can request for Movies and Web Series here ❤️.")

# async def request_commmand(update, context):
#   await update.message.reply_text("Ok i will look after that.")

async def welcome_command(update, context):
  chat_member = update.chat_member

  chat_title = chat_member.chat.title
  chat_member_first_name = chat_member.from_user.first_name
  new_chat_member_status = chat_member.new_chat_member.status
  old_chat_member_status = chat_member.old_chat_member.status
  # from_user_username = chat_member.from_user.username

  # Check if the user has joined
  if old_chat_member_status in ["left", "kicked"] and new_chat_member_status == "member":
    await update.effective_chat.send_message(f"Hey {chat_member_first_name} 👋🏻,\nWelcome to {chat_title} 🎉. Request Movies and Web Series here")

# Generic message handler for group messages
async def custom_commmand(update, context):
  user_id = update.effective_user.id
  chat_id = update.effective_chat.id
  chat_member = await context.bot.get_chat_member(chat_id, user_id)

  if chat_member.status == ChatMemberStatus.MEMBER:
    text = update.message.text
    if text is not None:
      await update.message.reply_text(f"I'll look for anything related to '{text}' and get back to you as soon as possible😊.")


# Main function
def main():
  app = ApplicationBuilder().token(API_TOKEN).build()

  app.add_handler(CommandHandler('start', start_commmand))
  # app.add_handler(CommandHandler('request', request_commmand))
  app.add_handler(ChatMemberHandler(welcome_command, ChatMemberHandler.CHAT_MEMBER))
  app.add_handler(MessageHandler(filters.Text and ~filters.COMMAND, custom_commmand))

  PORT = int(os.environ.get("PORT", 5000))
  WEBHOOK_URL = f"https://your-app-name.onrender.com/{API_TOKEN}"
  
  # Run bot
  app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=API_TOKEN,
    webhook_url=WEBHOOK_URL,
  )

if __name__ == "__main__":
  main()
