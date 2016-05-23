from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm
from datetime import datetime
from ..email import send_email



@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
#            and not current_user.confirmed \
#            and request.endpoint[:5] != 'auth.':
#        flash('You are not confirmed.')
#        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('main.index')
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout(): 
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/signup', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)# member_since=datetime.utcnow())
        print user.member_since
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm your Tavern Cellar account',
                   'auth/email/confirm', user=user, token=token)
        flash('A email has been sent to the given address. Please confirm your account.')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('Your confirmation link is invalid or expired.')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account', 
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to your email address.')
    return redirect(url_for('main.index'))

