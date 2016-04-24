from datetime import datetime
from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.moment import Moment

app = Flask(__name__)

manager = Manager(app)
moment = Moment(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user')
def user():
    return render_template('user.html')


@app.route('/srd')
def srd():
    return render_template('srd.html')


@app.route('/browse')
def browse():
    return render_template('browse.html')


@app.route('/submit')
def submit():
    return render_template('submit.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')

	

if __name__ == '__main__':
    manager.run()
