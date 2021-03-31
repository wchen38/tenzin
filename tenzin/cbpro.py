from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, flash, session, current_app
)
from werkzeug.exceptions import abort
from tenzin.crypto_lib.cbpro_weighted_api import CbproWeightedApi
import cbpro
from datetime import timedelta

bp = Blueprint('cbpro', __name__)

@bp.route('/', methods=["GET"])
def index():
    error_msg = None
    cbpro_data = None
    api = None
    # print("on refresh session: {}".format(session))
    # print("on refresh session life time: {}".format(current_app.permanent_session_lifetime))
    if "key" in session and "secret" in session and "passphrase" in session:
        key = session["key"]
        secret = session["secret"]
        passphrase = session["passphrase"]
        api = connect_to_cbpro(key, secret, passphrase)
        if api:
            api.get_realized_gain()
            api.get_appt()
            cbpro_data = api.workbook
            # cbpro_data = {'BTC-USD': {'2021-03-01T05:43:05.399Z': {'realized': -0.008851547094039439, 'average_profit': 0, 'average_loss': -0.008851547094039439, 'profit_probability': 0.0, 'appt': -0.008851547094039439}, '2021-03-14T20:41:45.37Z': {'realized': 0.23089632829473325, 'average_profit': 0.23089632829473325, 'average_loss': -0.008851547094039439, 'profit_probability': 0.5, 'appt': 0.11102239060034691}, '2021-03-17T07:05:41.012Z': {'realized': 0.00031244198717773333, 'average_profit': 0.11560438514095549, 'average_loss': -0.008851547094039439, 'profit_probability': 0.6666666666666666, 'appt': 0.07411907439595718}, '2021-03-20T21:28:40.367Z': {'realized': 0.0368616774337646, 'average_profit': 0.08935681590522519, 'average_loss': -0.008851547094039439, 'profit_probability': 0.75, 'appt': 0.06480472515540903}}}
            # cbpro_data.update({'ETH-USD': {'2021-03-01T05:44:05.399Z': {'realized': -0.008851547094039439, 'average_profit': 0, 'average_loss': -0.008851547094039439, 'profit_probability': 0.0, 'appt': -0.008851547094039439}, '2021-03-14T20:42:45.37Z': {'realized': 0.23089632829473325, 'average_profit': 0.23089632829473325, 'average_loss': -0.008851547094039439, 'profit_probability': 0.5, 'appt': 0.11102239060034691}, '2021-03-17T07:05:42.012Z': {'realized': 0.00031244198717773333, 'average_profit': 0.11560438514095549, 'average_loss': -0.008851547094039439, 'profit_probability': 0.6666666666666666, 'appt': 0.07411907439595718}, '2021-03-20T21:28:41.367Z': {'realized': 0.0368616774337646, 'average_profit': 0.08935681590522519, 'average_loss': -0.008851547094039439, 'profit_probability': 0.75, 'appt': 0.06480472515540903}}})
    else:
        flash("Please enter your keys.")

    data = {}
    data["message"] = ["hello", "world"]
    data["cbpro"] = cbpro_data
    return render_template('cbpro/index.html', flask_var=data)

@bp.route('/', methods=["POST"])
def index_post():
    key = request.form['api_key']
    secret = request.form['client_secret']
    passphrase = request.form['passphrase']


    # save the cbpro info to session
    # delete those values if they enter the wrong values again
    if connect_to_cbpro(key, secret, passphrase):
        session.permanent = True
        # current_app.permanent_session_lifetime = timedelta(seconds=5)
        print("setting session life time: {}".format(current_app.permanent_session_lifetime))
        session["key"] = key
        session["secret"] = secret
        session["passphrase"] = passphrase
        # print("++++++++++++++save input to session: {} {} {}".format(key, secret, passphrase))
    else:
        session.pop('key', None)
        session.pop('secret', None)
        session.pop('passphrase', None)

        error_msg = "Invalid API Key"
        print(error_msg)
        flash(error_msg)
    return redirect(url_for('cbpro.index'))

def connect_to_cbpro(key, secret, passphrase):
    # print("key: {}\nsecret: {}\npassphrase:{}".format(key, secret, passphrase))
    public_client = cbpro.PublicClient()
    api_url = current_app.config["CBPRO_API_URL"]
    auth_client = cbpro.AuthenticatedClient(key, secret, passphrase, api_url=api_url)
    api = CbproWeightedApi(public_client, auth_client)
    if api.is_valid_account():
        return api
    return None

def format_data(workbook):
    table = []
    for product_id, records in workbook.items():
        for date, record in records.items():
            row = []
            row.append(product_id)
            row.append(date)
            row.append(record["realized"])
            row.append(record["appt"])
            table.append(row)
    return table