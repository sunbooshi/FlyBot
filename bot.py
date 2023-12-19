from botutils import *
import gpt
import gemini as gem
from config import config

llm = 'gemini'

@CMD
def chatid(update: Update, context: CallbackContext):
    try:
        text = str(update.effective_chat.id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))

@CMD
def uid(update: Update, context: CallbackContext):
    try:
        user = update.message.from_user
        text = str(user.id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))

@CMD
def use(update: Update, context: CallbackContext):
    global llm
    if not check_admin(update, context): return
    args = context.args
    if len(args) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text='/use gpt \n/use gemini')
        return
    if args[0] == 'gpt':
        llm = 'gpt'
        context.bot.send_message(chat_id=update.effective_chat.id, text='change to gpt')
    elif args[0] == 'gemini':
        llm = 'gemini'
        context.bot.send_message(chat_id=update.effective_chat.id, text='change to gemini')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='/use gpt \n/use gemini')

@CMD
def reset(update: Update, context: CallbackContext):
    if not check_admin(update, context): return
    try:
        gem.reset_chat()
        context.bot.send_message(chat_id=update.effective_chat.id, text='reseted')
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))

max_conversion = 5
conversions = []
system_message = ''

@MSG
def chat(update: Update, context: CallbackContext):
    text = update.message.text
    resp = text
    user = update.message.from_user
    parse_mode = None
    global max_conversion, conversions, system_message
    if not check_admin(update, context): return
    try:
        resp = ''
        if llm == 'gpt':
            resp = gpt.chat_completion(text, str(user.id), 
                                conversions=conversions,
                                max_conversion=max_conversion,
                                system_message=system_message)
        elif llm == 'gemini':
            resp = gem.chat_completion(text, str(user.id), 
                                conversions=conversions,
                                max_conversion=max_conversion,
                                system_message=system_message)
        parse_mode = 'Markdown'
        context.bot.send_message(chat_id=update.effective_chat.id,
                text=resp,
                reply_to_message_id=update.message.message_id,
                parse_mode=parse_mode)
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))

def check_admin(update, context):
    admin_uid = config.ADMIN_UID
    uid = str(update.effective_user.id)
    if len(admin_uid) == 0:
        resp = 'config admin user by: export ADMIN_UID="Your telegram user id"'
    elif admin_uid == uid:
        resp = ''
    else: 
        resp = 'you cant talk with me.'

    if len(resp) > 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
        return False
    else:
        return True

def run():
    token = config.BOT_TOKEN
    if len(token) == 0:
        raise Exception('Bot token unset', 'set token by: export TEL_BOT_TOKEN="You bot token"')
    start_bot(token)

if __name__ == '__main__':
    run()
