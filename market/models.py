from market import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """User model class."""

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=50000)
    items = db.relationship('Item', backref='owned_user', lazy='dynamic')

    def can_sell(self, item_obj):
        """Check if the user can sell the given item."""
        return item_obj in self.items

    def can_purchase(self, item_obj):
        """Check if the user can purchase the given item."""
        return self.budget >= item_obj.price

    @property
    def pretty_budget(self):
        """Format budget in a pretty way."""
        if len(str(self.budget)) >= 4:
            return 'R {:,.2f}'.format(self.budget)
        else:
            return f'R {self.budget}'

    @property
    def password(self):
        """Get the user's password."""
        return self.password

    @password.setter
    def password(self, text_password):
        """Set the user's password."""
        self.password_hash = bcrypt.generate_password_hash(text_password).decode('utf-8')

    def check_password(self, attempted_password):
        """Check if the provided password is correct."""
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Item(db.Model):
    """Item model class."""
    
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def buy(self, user):
        """Buy the item."""
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        """Sell the item."""
        self.owner = None
        user.budget += self.price
        db.session.commit()

    def __repr__(self):
        """Representation of the item."""
        return f'Item {self.name}'

