from datetime import timedelta
class Config(object):
    TESTING = False
    TEST_KEY = "config base"
    CBPRO_API_URL = "https://api-public.sandbox.pro.coinbase.com"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)

class Production(Config):
    SECRET_KEY="prod" # change it in the future
    CBPRO_API_URL = "https://api.pro.coinbase.com"

class Development(Config):
    FLASK_ENV="development"
    SECRET_KEY="dev" #change it in the future

class Testing(Config):
    TESTING = True
