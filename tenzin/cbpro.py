from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('cbpro', __name__)

@bp.route('/')
def index():
    return render_template('cbpro/index.html')

@bp.route('/', methods=["POST"])
def show():
    # grab args from the user input
    key = request.form['api_key']
    secret = request.form['client_secret']
    passphrase = request.form['passphrase']

    print("key: {}\nsecret: {}\npassphrase:{}".format(key, secret, passphrase))
    
    # use the input to connect to coinbase API

    #process the API data

    # send it to the frontend
    data = {}
    data['test'] = ["hello", "world"]

    return data
