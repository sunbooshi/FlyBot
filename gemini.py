import google.generativeai as genai
from config import config
from md2tgmd import escape

GOOGLE_API_KEY= config.GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)

model = None
chat = None

def chat_completion(text:str, user:str, conversions:list=[], max_conversion:int=0, system_message:str='') -> str:
    if max_conversion > 0:
        chat.history = chat.history[-max_conversion:]
    
    chat.send_message(text)
    return escape(chat.last.text)

def reset_chat():
    global model, chat
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

reset_chat()