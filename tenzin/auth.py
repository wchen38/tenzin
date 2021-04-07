from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, flash, session, current_app
)
from . import (cbpro, oauth)

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('auth.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@bp.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    resp.raise_for_status()
    profile = resp.json()
    print(profile)
    # do something with the token and profile
    return redirect(url_for("cbpro.index"))


@bp.route('/hello')
def hello():
    return "<h1>hello</h1>"