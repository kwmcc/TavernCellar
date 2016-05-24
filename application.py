# application.py - for Elastic Beanstalk to easily start the server,
# this file should do essentially what "python manage.py runserver" does.

import os
from app import create_app, db

application = app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.secret_key= 'Secret'

if __name__ == "__main__":
    application.debug = True
    application.run(host='0.0.0.0')
