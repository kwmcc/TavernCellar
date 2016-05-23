import os
from flask import render_template, request, session, redirect, abort, url_for, current_app, flash
from flask.ext.script import Manager, Shell
#from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, FileField, TextField, TextAreaField
from wtforms.validators import Length
from werkzeug import secure_filename
from flask.ext.login import LoginManager, current_user, login_required
from .. import db
from ..models import SRD, User
from . import main
from ..__init__ import moment
from datetime import datetime

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


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/srd/<title>')
def srd(title):
	srd = SRD.query.filter_by(title=title).first_or_404()
	return render_template('srd.html', srd=srd)


@main.route('/browse')
def browse():
    return render_template('browse.html')

class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class SRDForm(Form):
	file = FileField('SRD .pdf')
	title = StringField("Title")
	description = TextField("Description")
	submit = SubmitField('Submit')

#This is currently really basic, but it does work.
#It redirects to the SRD page on submission
#we'll probably want to give the files numerical names
#to make it easier on ourselves and prevent duplicate uploads.
@main.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
	form = SRDForm()
        print (current_user)
	if form.validate_on_submit():
		filename = secure_filename(form.file.data.filename)
		title = form.title.data
		description = form.description.data
		srd = SRD()
		srd.title=title
		srd.filename=filename
		srd.description=description
		srd.submissiontime=datetime.utcnow()
		db.session.add(srd)
		form.file.data.save('uploads/' + filename)
		return redirect(url_for('main.srd', title=title))
	return render_template('submit.html', form=form)

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))    
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)
