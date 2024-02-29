from market import app, db
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from market.models import Item, User
from market.forms import RegisterForm
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
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
                                  password_hash=form.password1.data)
            db.session.add(user_to_create)
            db.session.commit()
            return redirect(url_for('market_page'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f'The was an error {err}', category='danger')
    else:
        print('no errors')
    return render_template('register.html', form=form)


