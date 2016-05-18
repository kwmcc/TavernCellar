#! /usr/bin/env python

#This script is used to launch the application 
import os 
from app import create_app, db
from app.models import User, SRD, Comment, Tag, Rating
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
#from flask.ext.mail import Mail

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.secret_key= 'Secret'
manager = Manager(app)
migrate = Migrate(app, db)
#mail = Mail(app)
app.config['SECRET_KEY'] = 'Secret'

#Likely temporary, uses a gmail account
#app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
#app.config['MAIL_PORT'] = 587
#app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USERNAME'] = 'itstaverncellar'
#app.config['MAIL_PASSWORD'] = 'taverncellar2102'

def make_shell_context():
    return dict(app=app, db=db, User=User, SRD=SRD, Comment=Comment,
                Tag=Tag, Rating=Rating)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    test = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
