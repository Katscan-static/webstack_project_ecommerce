from market import app, db
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellingForm
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    """Render the home page."""
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    """Render the market page."""
    purchase_form = PurchaseItemForm()
    selling_form = SellingForm()

    if request.method == "POST":
        # Purchase
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()

        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congrats! you purchased a {p_item_object.name} for {p_item_object.price}", category="success")
            else:
                flash('Not enough funds to purchase this item', category="danger")

        # Sell
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()

        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congrats! you sold a {s_item_object.name} to market for {s_item_object.price}", category="success")
            else:
                flash("Something went wrong")

        return redirect(url_for('market_page'))

    if request.method == 'GET':
        with app.app_context():
            items = Item.query.filter_by(owner=None)
            owned_items = Item.query.filter_by(owner=current_user.id)

    return render_template('market.html',
                           items=items,
                           purchase_form=purchase_form,
                           owned_items=owned_items,
                           selling_form=selling_form)


@app.route('/register', methods=['GET', 'POST'])
def registration_page():
    """Render the registration page."""
    form = RegisterForm()

    if form.validate_on_submit():
        with app.app_context():
            user_to_create = User(username=form.username.data,
                                  email=form.email_address.data,
                                  password=form.password1.data)
            db.session.add(user_to_create)
            db.session.commit()
            login_user(user_to_create)
            flash(f'Successfully registered, you are now logged in as {user_to_create.username}', category="info")
            return redirect(url_for('market_page'))

    if form.errors != {}:
        for err in form.errors.values():
            flash(f'The was an error {err}', category='danger')
    else:
        print('no errors')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """Render the login page."""
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
    """Logout the user."""
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('home_page'))

