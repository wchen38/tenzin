import os
from datetime import timedelta


class Config(object):
    TESTING = False
    CBPRO_API_URL = "https://api-public.sandbox.pro.coinbase.com"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)

    '''
    keys to add in a local config.py file
        SECRET_KEY
        GOOGLE_CLIENT_ID
        GOOGLE_CLIENT_SECRET
        DB_NAME
        DB_USERNAME
        DB_PASSWORD
    '''


class Production(Config):
    CBPRO_API_URL = "https://api.pro.coinbase.com"
    ENVIRONMENT = "production"


class Development(Config):
    SECRET_KEY = "dev"  # change it in the future
    ENVIRONMENT = "development"
    DB_NAME = "tenzin_db_dev"
    DB_USERNAME = 'dev'
    DB_PASSWORD = 'dev'


class Testing(Config):
    TESTING = True
    ENVIRONMENT = "testing"
