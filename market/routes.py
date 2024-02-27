@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    with app.app_context():
        items = Item.query.all()
    return render_template('market.html', items=items)

