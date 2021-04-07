import os
import pdb

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from authlib.integrations.flask_client import OAuth
from datetime import timedelta

csrf = CSRFProtect()
oauth = OAuth()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    csrf.init_app(app)
    oauth.init_app(app)
    config = os.environ['CONFIG_SETUP']
    try:
        app.config.from_pyfile('config.py')
    except Exception:
        pass
    app.config.from_object(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    print("=======================")
    print("export environment: {}".format(app.config['ENVIRONMENT']))
    print("=======================")
    GOOGLE = oauth.register(
        name='google',
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
        client_kwargs={'scope': 'openid email profile'},
    )

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import cbpro
    app.register_blueprint(cbpro.bp)
    app.add_url_rule('/', endpoint='index')

    from . import auth
    app.register_blueprint(auth.bp)

    return app
