import os

class Config(object):
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 8080))
    DEBUG = int(os.environ.get('DEBUG', 0)) == 1
    BOT_TOKEN = os.environ.get('TEL_BOT_TOKEN', '')
    ADMIN_UID = os.environ.get('ADMIN_UID', '')
    WEB_TOKEN = os.environ.get('WEB_TOKEN', '')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    GPT_MODEL = os.environ.get('GPT_MODEL', 'gpt-3.5-turbo')
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')

config = Config()
