import os
from dotenv import load_dotenv
from os import environ

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


def as_bool(value):
    if value:
        return value.lower() in ['true', 'yes', 'on', '1']
    return False


class BaseConfig(object):
    # database options
    DB_USERNAME = os.environ['DB_USERNAME']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_HOST = os.environ['DB_HOST']
    DATABASE_NAME = os.environ['DATABASE_NAME']
    DB_PORT = os.environ['DB_PORT']
    ALCHEMICAL_DATABASE_URL = "mysql+pymysql://%s:%s@%s:%s/%s" % (
        DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DATABASE_NAME)
    ALCHEMICAL_ENGINE_OPTIONS = {'echo': as_bool(os.environ.get('SQL_ECHO'))}
    ALCHEMICAL_ECHO = True

    # security options
    SECRET_KEY = os.environ.get('SECRET_KEY', 'top-secret!')
    DISABLE_AUTH = as_bool(os.environ.get('DISABLE_AUTH'))
    ACCESS_TOKEN_MINUTES = int(os.environ.get('ACCESS_TOKEN_MINUTES') or '15')
    REFRESH_TOKEN_DAYS = int(os.environ.get('REFRESH_TOKEN_DAYS') or '7')
    REFRESH_TOKEN_IN_COOKIE = as_bool(os.environ.get(
        'REFRESH_TOKEN_IN_COOKIE') or 'yes')
    REFRESH_TOKEN_IN_BODY = as_bool(os.environ.get('REFRESH_TOKEN_IN_BODY'))
    RESET_TOKEN_MINUTES = int(os.environ.get('RESET_TOKEN_MINUTES') or '15')
    PASSWORD_RESET_URL = os.environ.get('PASSWORD_RESET_URL') or \
        'http://localhost:3000/reset'
    USE_CORS = as_bool(os.environ.get('USE_CORS') or 'yes')
    CORS_SUPPORTS_CREDENTIALS = True

    # API documentation
    APIFAIRY_TITLE = 'National Export Trade Promotion API'
    APIFAIRY_VERSION = 'V1.0'
    APIFAIRY_UI = os.environ.get('DOCS_UI', 'elements')

    # email options
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or '25')
    MAIL_USE_TLS = as_bool(os.environ.get('MAIL_USE_TLS'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER',
                                         'donotreply@microblog.example.com')


class ProdConfig(BaseConfig):
    ENV = 'production'
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    DB_USERNAME = os.environ['PROD_DB_USERNAME']
    DB_PASSWORD = os.environ['PROD_DB_PASSWORD']
    DB_HOST = os.environ['PROD_DB_HOST']
    DATABASE_NAME = os.environ['PROD_DATABASE_NAME']
    ALCHEMICAL_DATABASE_URL = "mysql+pymysql://%s:%s@%s:3306/%s" % (
        DB_USERNAME, DB_PASSWORD, DB_HOST, DATABASE_NAME)
    ALCHEMICAL_ENGINE_OPTIONS = {'echo': as_bool(os.environ.get('SQL_ECHO'))}

    # security options
    SECRET_KEY = os.environ.get('SECRET_KEY', 'top-secret!')
    DISABLE_AUTH = as_bool(os.environ.get('DISABLE_AUTH'))
    ACCESS_TOKEN_MINUTES = int(os.environ.get('ACCESS_TOKEN_MINUTES') or '15')
    REFRESH_TOKEN_DAYS = int(os.environ.get('REFRESH_TOKEN_DAYS') or '7')
    REFRESH_TOKEN_IN_COOKIE = as_bool(os.environ.get(
        'REFRESH_TOKEN_IN_COOKIE') or 'yes')
    REFRESH_TOKEN_IN_BODY = as_bool(os.environ.get('REFRESH_TOKEN_IN_BODY'))
    RESET_TOKEN_MINUTES = int(os.environ.get('RESET_TOKEN_MINUTES') or '15')
    PASSWORD_RESET_URL = os.environ.get('PASSWORD_RESET_URL') or \
        'http://localhost:3000/reset'
    USE_CORS = as_bool(os.environ.get('USE_CORS') or 'yes')
    CORS_SUPPORTS_CREDENTIALS = True
    JSON_SORT_KEYS = False

    # API documentation
    APIFAIRY_TITLE = 'National Export Trade Promotion API'
    APIFAIRY_VERSION = '1.0'
    APIFAIRY_UI = os.environ.get('DOCS_UI', 'elements')
    APIFAIRY_UI_PATH = '/api/docs'
    # APIFAIRY_TAGS = ['tokens_guest', 'booking', 'rooms', 'guests', 'restaurant']

    # email options
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or '25')
    MAIL_USE_TLS = as_bool(os.environ.get('MAIL_USE_TLS'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER',
                                         'no-reply@eminpasha.com')
