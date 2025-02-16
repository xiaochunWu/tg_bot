from telegram.ext import Updater, MessageHandler, Filters

# 替换为你的 Telegram Bot Token
TOKEN = '7851775832:AAEtuGXRVLa4VJmKcd6W3BAP7KQGlPv2TEU'

def get_group_id(update, context):
    chat_id = update.effective_chat.id
    print(f"group ID is: {chat_id}")

# bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

group_id_handler = MessageHandler(Filters.all, get_group_id)
dispatcher.add_handler(group_id_handler)

updater.start_polling()
updater.idle()