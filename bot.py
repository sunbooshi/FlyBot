from botutils import *
from gpt import chat_completion
from config import config

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


max_conversion = 5
conversions = []
system_message = ''

@MSG
def chat(update: Update, context: CallbackContext):
    admin_uid = config.ADMIN_UID
    text = update.message.text
    resp = text
    user = update.message.from_user
    parse_mode = None
    global max_conversion, conversions, system_message
    try:
        print(user.id)
        if len(admin_uid) == 0:
            resp = 'config admin user by: export ADMIN_UID="Your telegram user id"'
        elif admin_uid == str(user.id):
            resp = chat_completion(text, str(user.id), 
                                   conversions=conversions,
                                   max_conversion=max_conversion,
                                   system_message=system_message)
            parse_mode = 'Markdown'
        else: 
            resp = 'you cant talk with me.'
        context.bot.send_message(chat_id=update.effective_chat.id,
                text=resp,
                reply_to_message_id=update.message.message_id,
                parse_mode=parse_mode)
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))

def run():
    token = config.BOT_TOKEN
    if len(token) == 0:
        raise Exception('Bot token unset', 'set token by: export TEL_BOT_TOKEN="You bot token"')
    start_bot(token)

if __name__ == '__main__':
    run()
