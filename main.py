from bot import run
from web import app
from config import config
import threading


def web_server():
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)

def main():
    # start web server
    threading.Thread(target=web_server, name='Web').start()

    # start bot 
    run()


if __name__ == '__main__':
    main()