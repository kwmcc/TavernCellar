import os
from datetime import datetime
from flask import Flask, render_template, session, request, redirect, url_for, send_from_directory
from flask.ext.script import Manager, Shell
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.migrate import Migrate, MigrateCommand
from werkzeug import secure_filename, generate_password_hash, check_password_hash

#setup for database
basedir = os.path.abspath(os.path.dirname(__file__))

#setup for uploads to work
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['pdf'])

#setup for login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

#app itself
app = Flask(__name__)
app.debug = True
app.secret_key= 'Secret'

#setup for uploads to work
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#setup for database to work
app.config['SQLALCHEMY_DATABASE_URI'] =\
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#setup for some app functionality
manager = Manager(app)
moment = Moment(app)
migrate = Migrate(app, db)

#adds the shell command to the Manager
def make_shell_context():
    return dict(app=app, db=db, User=User, SRD=SRD, Comment=Comment, Tag=Tag, Rating=Rating)
manager.add_command("shell", Shell(make_context=make_shell_context))

#adds the migrate command to Manager
manager.add_command('db', MigrateCommand)

#DATABASE
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username

class SRD(db.Model):
	__tablename__ = 'srd'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	filename = db.Column(db.String(64))
	description = db.Column(db.Text)
	reported = db.Column(db.Boolean)
	submissiontime = db.Column(db.DateTime)

	def __repr__(self):
		return '<SRD %r>' % self.title

class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	srd_id = db.Column(db.Integer, db.ForeignKey('srd.id'))
	content = db.Column(db.Text)
	posttime = db.Column(db.DateTime)

	def __repr__(self):
		return '<Comment %r>' % self.id

class Tag(db.Model):
	__tablename__ = 'tags'
	id = db.Column(db.Integer, primary_key=True)
	srd_id = db.Column(db.Integer, db.ForeignKey('srd.id'))
	content = db.Column(db.String(64))

	def __repr__(self):
		return '<Tag %r>' % self.content

class Rating(db.Model):
	__tablename__ = 'ratings'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	srd_id = db.Column(db.Integer, db.ForeignKey('srd.id'))
	value = db.Column(db.Integer, default = 0)#1 if positive, -1 if negative rating

	def __repr__(self):
		return '<Rating %r>' % self.value

#used for getting information for currently logged in users.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#sutup for uploads
#checks if the file is an allowed file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


################### ERROR HANDLING AND ROUTES ####################	
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#home page
#Currently known as "The Bar"
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

class SRDForm(Form):
	file = FileField('SRD .pdf')
	title = StringField("Title")
	submit = SubmitField('Submit')

#This is currently really basic, but it does work.
#It redirects to the SRD page on submission
#we'll probably want to give the files numerical names
#to make it easier on ourselves and prevent duplicate uploads.
@app.route('/submit', methods=['GET', 'POST'])
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
		return redirect(url_for('srd', srd=srd))
	return render_template('submit.html', form=form)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')





if __name__ == '__main__':
    manager.run()
