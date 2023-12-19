import openai
import enum
from config import config

openai.api_key = config.OPENAI_API_KEY

class Role(enum.Enum):
    User = 'user'
    System = 'system'
    Assistant = 'assistant'

def build_message(role:Role, content:str) -> dict:
    return {'role': role.value, 'content':content}


def chat_completion(text:str, user:str, conversions:list=[], max_conversion:int=0, system_message:str='') -> str:
    messages = []

    if max_conversion > 0:
        conversions = conversions[-max_conversion:]
        messages.extend(conversions)
    
    user_message = build_message(Role.User, text)
    messages.append(user_message)
    conversions.append(user_message)

    if len(system_message) > 0:
        messages.append(build_message(Role.System, system_message))
    
    response = openai.ChatCompletion.create(model=config.GPT_MODEL, messages=messages, temperature=0.2, user=user)
    choices = response['choices'][0]
    message = choices['message']
    assistant_message = message['content']
    conversions.append(build_message(Role.Assistant, assistant_message))
    return assistant_message