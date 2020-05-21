from app import app, db, sockIO
from models import User
from forms import LoginForm, RegistrationForm
from flask import redirect, url_for, request, flash, render_template
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
@app.route('/index')
def index():
    posts = list()
    return render_template("index.html",
                           title='Home',
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_pwd(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_pwd(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you\'ve joined a gay club!')
        return redirect(url_for('login'))
    return render_template('register.html',
                           title='Join the Dark Side',
                           form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',
                           title=username,
                           user=user,
                           posts=posts)


@app.route('/sessions')
@login_required
def sessions():
    return render_template('sessions.html')


def message_received(methods=['GET','POST']):
    print('message received')


@sockIO.on('my event')
def handle_event(json, methods=['GET', 'POST']):
    print('received event: ' + str(json))
    sockIO.emit('my response', json, callback=message_received)
