import logging
from functools import wraps

from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import Update


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

msg_handlers = {}
cmd_handlers = {}

def MSG(func):
    name = func.__name__
    if name in msg_handlers.keys():
        raise Exception(f'function {name} alreay exists.')
    else:
        msg_handlers[name] = func
    @wraps(func)
    def decorated(*args, **kwargs):
        return func(*args, **kwargs)
    return decorated

def CMD(func):
    name = func.__name__
    if name in cmd_handlers.keys():
        raise Exception(f'function {name} alreay exists.')
    else:
        cmd_handlers[name] = func
    @wraps(func)
    def decorated(*args, **kwargs):
        return func(*args, **kwargs)
    return decorated

@CMD
def help(update: Update, context: CallbackContext):
    msg = 'all cmds:\n'
    for key in cmd_handlers.keys():
        msg = msg + '/' + key + '\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
 
def text_dispatcher(update:Update, context:CallbackContext):
    for key in msg_handlers.keys():
        msg_handlers[key](update, context)

def start_bot(token:str):
    updater = Updater(token=token, use_context=True)

    dispatcher = updater.dispatcher
    text_handler = MessageHandler(Filters.text & (~Filters.command), text_dispatcher)
    dispatcher.add_handler(text_handler)

    for key in cmd_handlers.keys():
        handler = CommandHandler(key, cmd_handlers[key])
        dispatcher.add_handler(handler)

    updater.start_polling()
    updater.idle()