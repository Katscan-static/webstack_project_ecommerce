from market import app, db
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from market.models import Item, User
from market.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
@
def market_page():
    with app.app_context():
        items = Item.query.all()
    return render_template('market.html', items=items)


@app.route('/register', methods=['GET', 'POST'])
def registration_page():
    form = RegisterForm()
    if form.validate_on_submit():
        with app.app_context():
            user_to_create = User(username=form.username.data,
                                  email=form.email_address.data,
                                  password=form.password1.data)
            db.session.add(user_to_create)
            db.session.commit()
            return redirect(url_for('market_page'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f'The was an error {err}', category='danger')
    else:
        print('no errors')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        with app.app_context():
            attempted_user = User.query.filter_by(username=form.username.data).first()
            print(form.username.data)
            print(attempted_user)
            if attempted_user and attempted_user.check_password(
                    attempted_password=form.password.data):
                login_user(attempted_user)
                flash(f'You are succesfully logged in: {attempted_user.username}', category='success')
                return redirect(url_for('market_page'))
            else:
                flash('Username or password incorrect please try again', category='danger')

    return render_template('login.html', form=form) 

@app.route('/logout')
def logout_page():
    logout_user()
    flash('you have been logged out', category='info')
    return redirect(url_for('home_page'))
