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
    '''

class Production(Config):
    CBPRO_API_URL = "https://api.pro.coinbase.com"

class Development(Config):
    SECRET_KEY="dev" #change it in the future

class Testing(Config):
    TESTING = True
