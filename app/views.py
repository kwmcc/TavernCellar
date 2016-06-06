#WHOOSH

from flask import render_template, redirect, request, url_for, flash, g, session
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm, SearchForm
from datetime import datetime
from ..email import send_email
from config import MAX_SEARCH_RESULTS

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/search', methods=['POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('browse', query=g.search_form.search.data))

@app.route('/browse/<query>')
def browse(query):
    results = SRD.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('browse.html',
                           query=query,
                           results=results)