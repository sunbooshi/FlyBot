import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import config
from gpt import chat_completion
import enum

max_conversion = 5
conversions = []
system_message = ''

app = Flask(__name__)

CORS(app)

class RespStatus(enum.IntEnum):
    Success = 0
    InteralException = 100
    InvaildParams = 101
    InvaildRequest = 102

def sucess_resp(data:dict):
    return jsonify({"status": RespStatus.Success, "msg":"OK", "result":data})

def fail_resp(code:int, msg:str):
    return jsonify({"status":code, "msg":msg})

def except_resp(e):
    return jsonify({"status": RespStatus.InteralException, "msg": "exception"})

@app.get('/api/status')
def status():
    return 'OK'

@app.post('/api/chat')
def chat():
    try:
        token = request.headers.get('Token')
        if token is None or token != config.WEB_TOKEN:
            return fail_resp(RespStatus.InvaildRequest, 'access denied')

        text = None
        if 'text' in request.json:
            text = request.json['text']

        if text is None or len(text) == 0:
            return fail_resp(RespStatus.InvaildParams, 'text needed')

        resp = chat_completion(text, 'web',
                               conversions=conversions,
                               max_conversion=max_conversion,
                               system_message=system_message)
        return sucess_resp({'response': resp})

    except Exception as e:
        app.logger.error(str(e) + '\n' + traceback.format_exc())
        return except_resp(e)

@app.get('/')
def index():
    return '<h1>Hello, FlyBot!</h1>'
