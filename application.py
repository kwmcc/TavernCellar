from flask import Flask

application = app = Flask(__name__)

if __name__ == "__main__":
    application.run(host='0.0.0.0')
