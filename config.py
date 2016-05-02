import os 
basedir = os.path.abspath(os.path.dirname(__file__))

class Config: 
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #setup for uploads to work 
    #UPLOAD_FOLDER = 'uploads/'
    #ALLOWED_EXTENSIONS = set(['pdf'])

    @staticmethod
    def init_app(app):
        pass

#   These classes enable the application to run under different configurations, 
#each using a different database. 
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


#   two simple unit tests are defined in tests/test_basics.py
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development' : DevelopmentConfig,

    'testing' : TestingConfig, 
    'production' : ProductionConfig,
    'default' : DevelopmentConfig
}
