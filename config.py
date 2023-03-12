import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # General Configs
    TITLE = 'TriviaMaster'
    SECRET_KEY = 'secret'
    SQLALCHEMY_TRACK_NOTIFICATIONS = False
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    ITEMS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev-data.sqlite')
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test-data.sqlite')
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'prod-data.sqlite')
    PRODUCTION = True


config = {
    'default': DevelopmentConfig,
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}