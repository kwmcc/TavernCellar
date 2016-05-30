# application.py - for Elastic Beanstalk to easily start the server,
# this file should do essentially what "python manage.py runserver" does.

import os
from app import create_app, db
#from migrate.versioning import api
#from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO

application = app = create_app(os.getenv('FLASK_CONFIG') or 'production')
app.secret_key= 'Secret'

# def db_create():
#     db.create_all()
#     if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
#         api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
#         api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
#     else:
#         api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))


if __name__ == "__main__":
    with app.app_context():
        #db.drop_all()
        db.create_all()
    application.debug = False
    application.run(host='0.0.0.0')
