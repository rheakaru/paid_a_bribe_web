from flask import Flask
application = Flask(__name__)
from paid_a_bribe import web_app

@application.route('/')
def homepage():
    return "If you give me your state - I will tell you if ipaidabribe.com recently received a report from that state. Try me!"

@application.route('/<state>')
def run_app(state):
    msg = web_app(state)
    return msg
    #return "hello pt2"

if __name__ == '__main__':
    application.run(debug=True, use_reloader=True)
