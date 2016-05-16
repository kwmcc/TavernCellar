import os
from flask import render_template, request, session, redirect, url_for, current_app
from flask.ext.script import Manager, Shell
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, FileField
from werkzeug import secure_filename
from flask.ext.login import LoginManager
from .. import db
from ..models import SRD
from . import main

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['pdf']) 

#used for getting information for currently logged in users.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#sutup for uploads
#checks if the file is an allowed file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#home page
#Currently known as "The Bar"
@main.route('/')
def index():
    return render_template('index.html')


@main.route('/user')
def user():
    return render_template('user.html')


@main.route('/srd/<title>')
def srd(title):
	srd = SRD.query.filter_by(title=title).first_or_404()
	return render_template('srd.html', srd=srd)


@main.route('/browse')
def browse():
    return render_template('browse.html')


class SRDForm(Form):
	file = FileField('SRD .pdf')
	title = StringField("Title")
	submit = SubmitField('Submit')

#This is currently really basic, but it does work.
#It redirects to the SRD page on submission
#we'll probably want to give the files numerical names
#to make it easier on ourselves and prevent duplicate uploads.
@main.route('/submit', methods=['GET', 'POST'])
def submit():
	form = SRDForm()
	if form.validate_on_submit():
		filename = secure_filename(form.file.data.filename)
		title = form.title.data
		srd = SRD()
		srd.title=title
		srd.filename=filename
		db.session.add(srd)
		form.file.data.save('uploads/' + filename)
		return redirect(url_for('main.srd', title=title))
	return render_template('submit.html', form=form)


@main.route('/login')
def login():
    return render_template('login.html')


@main.route('/signup')
def signup():
    return render_template('signup.html')
