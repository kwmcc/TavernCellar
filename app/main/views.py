import os
import sys
from flask import render_template, request, session, redirect, url_for, current_app, send_from_directory
from flask.ext.script import Manager, Shell
from werkzeug import secure_filename
from flask.ext.login import LoginManager, current_user, login_required
from .. import db
from .forms import SRDForm
from ..models import User, SRD, Comment, Tag, TagTable, Rating
from . import main
from ..__init__ import moment
from datetime import datetime
from sqlalchemy import or_, exists
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
	tag_ids = TagTable.query.filter_by(srd_id=srd.id).all()
	ids = [];
	tags = None;
     	for id in tag_ids:
		ids.append(id.tag_id);
	if len(ids) > 0:
                tags = Tag.query.filter(or_(Tag.id == v for v in ids)).all()
        return render_template('srd.html', srd=srd, tags=tags)

@main.route('/view/<path:filename>')
def return_files_tut(filename):
	path = os.path.abspath('uploads/')
	return send_from_directory(path, filename)

@main.route('/browse')
def browse():
    return render_template('browse.html')


@main.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
	form = SRDForm()
	if form.validate_on_submit():
		filename = str(SRD.query.count()) + '.pdf'
		title = form.title.data
		description = form.description.data
		srd = SRD()
		srd.title=title
		srd.filename = filename
		srd.description=description
		srd.submissiontime=datetime.utcnow()
		db.session.add(srd)
		db.session.commit()
		form.file.data.save('uploads/' + filename)
                for tag in form.tag.data:
                    srd_tags = TagTable()
                    srd_tags.srd_id = srd.id  
                    new_tag = db.session.query(Tag).filter_by(content=tag).first()
                    if (new_tag):
                        srd_tags.tag_id = new_tag.id
                    else:
                        new_tag = Tag()
                        new_tag.content = tag
                        db.session.add(new_tag)
                        db.session.commit()
                        srd_tags.tag_id = new_tag.id
                    db.session.add(srd_tags)
                    db.session.commit() 
		return redirect(url_for('main.srd', title=title))
	return render_template('submit.html', form=form)

#Now defined in app/auth/views.py:

#@main.route('/login')
#def login():
#    return render_template('login.html')
#
#@main.route('/signup')
#def signup():
#    return render_template('auth/signup.html')

