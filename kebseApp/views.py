from datetime import datetime

from flask import render_template, flash, redirect, g, url_for
from flask_login import logout_user, login_required
from flask_login import login_user, current_user
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from werkzeug.security import generate_password_hash

from kebseApp import mail, lm, app, db
from kebseApp.forms import LoginForm, RegistrationForm
from flask_mail import Message

from kebseApp.logic import get_concate_username
from kebseApp.models import User
from kebseApp.oauth import OAuthSignIn


def send_mail(address):
    with mail.connect() as conn:
        msg = Message(subject="Test", sender="kebseSystem@yandex.ru", recipients=[address])
        msg.body = "Hello"
        msg.html = "<h1>kebsetest</h1>"
        conn.send(msg)


@lm.user_loader
def load_user(local_id):
    return User.query.get(int(local_id))


@app.route('/user/<user_id>')
@login_required
def hello_world(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user is None:
        flash('User ' + user_id + ' not found.')
        return redirect(url_for("sign_up"))
    return render_template('index.html', user=user)


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect("user/" + current_user.username)
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        try:
            user = User(username=form.username.data,
                        email=form.email.data,
                        password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            flash("Имя пользователя или почта уже используются")
            return redirect("signup")
        except PendingRollbackError:
            flash("Имя пользователя или почта уже используются")
            return redirect("signup")
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)
        return redirect("user/" + current_user.username)
    return render_template("signup.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('login')


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('login'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('login'))
    oauth = OAuthSignIn.get_provider(provider)
    user_id, token = oauth.callback()
    if user_id is None:
        flash('Authentication failed.')
        return redirect(url_for('login'))
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        username = get_concate_username(token, user_id)

        user = User(user_id=user_id, token=token, username=username)
        db.session.add(user)
        db.session.commit()

    login_user(user, True)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("user/" + current_user.user_id)
    form = LoginForm()
    return render_template("login.html", form=form)


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        print(11111)
        g.user.last_seen = datetime.now()
        db.session.add(g.user)
        db.session.commit()


@app.route('/')
def hello():
    return render_template('hello.html')


@app.route('/home')
def home():
    name = "Name"
    return render_template('index.html', name=name)
