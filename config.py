import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    #setup for uploads to work
    #UPLOAD_FOLDER = 'uploads/'
    #ALLOWED_EXTENSIONS = set(['pdf'])
    #Likely temporary, uses a gmail account
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'itstaverncellar'
    MAIL_PASSWORD = 'taverncellar2102'
    MAIL_SUBJECT_PREFIX = '[Tavern Cellar]'
    MAIL_SENDER = 'Tavern Cellar Admin <itstaverncellar@gmail.com>'
    #ADMIN = os.environ.get('ADMIN')

    @staticmethod
    def init_app(app):
        pass

#These classes enable the application to run under different configurations,
#each using a different database.
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


#two simple unit tests are defined in tests/test_basics.py
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

#debug-off, testing-off configuration for deployment
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig
}
