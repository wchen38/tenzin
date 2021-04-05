import os
import pdb

from flask import Flask
from flask_wtf.csrf import CsrfProtect
from datetime import timedelta

csrf = CsrfProtect()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    csrf.init_app(app)
    config = os.environ['CONFIG_SETUP']
    app.config.from_object(config)
    try:
        app.config.from_pyfile('config.py')
    except Exception:
        pass
    print(f"==========================")
    print(f"Environment: {app.config['FLASK_ENV']}")
    print(f"Debug: {app.config['DEBUG']}")
    print(f"Secret key: {app.config['SECRET_KEY']} (please change this in the future)")
    print(f"test config: {app.config['TEST_KEY']}")
    print(f"==========================")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import cbpro
    app.register_blueprint(cbpro.bp)
    app.add_url_rule('/', endpoint='index')

    return app