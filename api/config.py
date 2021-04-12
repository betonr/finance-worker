import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_settings(env):
    return CONFIG.get(env)


class Config():
    DEBUG = False
    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    URL_PROVIDER_FUNDAMENTUS = os.environ.get('URL_PROVIDER_FUNDAMENTUS', 'https://www.fundamentus.com.br')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'postgresql://{}:{}@{}:{}/{}'.format(
        os.environ.get('DB_USER', 'postgres'),
        os.environ.get('DB_PASSWORD', 'postgres2020'),
        os.environ.get('DB_HOST', 'localhost'),
        os.environ.get('DB_PORT', '5431'),
        os.environ.get('DB_DBNAME', 'finance')))
    session_id = os.environ.get('FUNDAMENTUS_SESSION_ID', 'a018f8045f46f3cbeee6fe4afac0a1bc')


class ProductionConfig(Config):
    """Production Mode."""

    DEBUG = False


class DevelopmentConfig(Config):
    """Development Mode."""

    DEVELOPMENT = True


class TestingConfig(Config):
    """Testing Mode (Continous Integration)."""
    TESTING = True
    DEBUG = True


CONFIG = {
    "DevelopmentConfig": DevelopmentConfig(),
    "ProductionConfig": ProductionConfig(),
    "TestingConfig": TestingConfig()
}
