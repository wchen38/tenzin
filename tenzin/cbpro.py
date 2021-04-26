from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, flash, session, current_app
)
from flask_wtf import FlaskForm
from flask_login import current_user
from werkzeug.exceptions import abort
from .crypto_lib.cbpro_weighted_api import CbproWeightedApi
from .models import User, Portfolio
import cbpro
from datetime import timedelta

bp = Blueprint('cbpro', __name__)


@bp.route('/', methods=["GET"])
def index():
    error_msg = None
    cbpro_data = None
    api = None

    form = FlaskForm()

    if current_user.is_authenticated:
        flash("you have logged in!")
        cbpro_data = load_from_session()
        if cbpro_data is None:
            cbpro_data = load_from_db()
        if cbpro_data is None:
            flash("Please enter your keys.")
    elif "data" in session:
        cbpro_data = session["data"]
        # cbpro_data = {'BTC-USD': {'2021-03-01T05:43:05.399Z': {'realized': -0.008851547094039439, 'average_profit': 0, 'average_loss': -0.008851547094039439, 'profit_probability': 0.0, 'appt': -0.008851547094039439}, '2021-03-14T20:41:45.37Z': {'realized': 0.23089632829473325, 'average_profit': 0.23089632829473325, 'average_loss': -0.008851547094039439, 'profit_probability': 0.5, 'appt': 0.11102239060034691}, '2021-03-17T07:05:41.012Z': {'realized': 0.00031244198717773333, 'average_profit': 0.11560438514095549, 'average_loss': -0.008851547094039439, 'profit_probability': 0.6666666666666666, 'appt': 0.07411907439595718}, '2021-03-20T21:28:40.367Z': {'realized': 0.0368616774337646, 'average_profit': 0.08935681590522519, 'average_loss': -0.008851547094039439, 'profit_probability': 0.75, 'appt': 0.06480472515540903}}}
        # cbpro_data.update({'ETH-USD': {'2021-03-01T05:44:05.399Z': {'realized': -0.008851547094039439, 'average_profit': 0, 'average_loss': -0.008851547094039439, 'profit_probability': 0.0, 'appt': -0.008851547094039439}, '2021-03-14T20:42:45.37Z': {'realized': 0.23089632829473325, 'average_profit': 0.23089632829473325, 'average_loss': -0.008851547094039439, 'profit_probability': 0.5, 'appt': 0.11102239060034691}, '2021-03-17T07:05:42.012Z': {'realized': 0.00031244198717773333, 'average_profit': 0.11560438514095549, 'average_loss': -0.008851547094039439, 'profit_probability': 0.6666666666666666, 'appt': 0.07411907439595718}, '2021-03-20T21:28:41.367Z': {'realized': 0.0368616774337646, 'average_profit': 0.08935681590522519, 'average_loss': -0.008851547094039439, 'profit_probability': 0.75, 'appt': 0.06480472515540903}}})
    else:
        flash("Please enter your keys.")
    data = {}
    # data["message"] = ["hello", "world"]
    data["cbpro"] = cbpro_data
    return render_template('index.html', flask_var=data, form=form)


@bp.route('/', methods=["POST"])
def index_post():
    key = request.form['api_key']
    secret = request.form['client_secret']
    passphrase = request.form['passphrase']

    api = connect_to_cbpro(key, secret, passphrase)
    if api is None:
        session.pop("data", None)
        error_msg = "Invalid API Key"
        print(error_msg)
        flash(error_msg)

        return redirect(url_for('cbpro.index'))

    session.permanent = True
    if current_user.is_authenticated:
        user = User.objects(user_id=current_user.user_id)[0]
        p_list = Portfolio.objects(user=user)
        if len(p_list) == 0:
            cbpro_data, latest_trade_id_map = make_call_to_all_apis(api)
            Portfolio(user=user, appt=cbpro_data, latest_trade_id_map=latest_trade_id_map).save()
        else:
            p = p_list[0]
            latest_cbpro_data, latest_trade_id_map = make_call_to_all_apis(api, latest_trade_id_map=p.latest_trade_id_map)
            # latest_cbpro_data = {"BTC-USD": {"hello": "world"}, "ETH-USD": {"hello": "eth"}}
            for product_id, info in latest_cbpro_data.items():
                if product_id in p.appt.keys():
                    p.appt[product_id].update(info)
                else:
                    p.appt[product_id] = info
            cbpro_data = p.appt
            Portfolio.objects(user=user).update_one(appt=cbpro_data)
            Portfolio.objects(user=user).update_one(latest_trade_id_map=latest_trade_id_map)
    else:
        cbpro_data, _ = make_call_to_all_apis(api)

    session["data"] = cbpro_data

    return redirect(url_for('cbpro.index'))


def connect_to_cbpro(key, secret, passphrase):
    public_client = cbpro.PublicClient()
    api_url = current_app.config["CBPRO_API_URL"]
    auth_client = cbpro.AuthenticatedClient(key, secret, passphrase, api_url=api_url)
    api = CbproWeightedApi(public_client, auth_client)
    if api.is_valid_account():
        return api
    return None


def make_call_to_all_apis(api, latest_trade_id_map=None):
    api.get_realized_gain(latest_trade_id_map=latest_trade_id_map)
    api.get_appt()
    return api.workbook, api.latest_fills_map


def load_from_session():
    if "data" in session:
        return session["data"]
    return None


def load_from_db():
    user = User.objects(user_id=current_user.user_id)[0]
    # user logged in, but haven't enter their API keys yet,
    # therefore, the Portfolio in database is empty.
    try:
        p = Portfolio.objects(user=user)[0]
        if len(p.appt) != 0:
            return p.appt
    except IndexError:
        pass
    return None
