#!/usr/bin/python3
""" Market python file"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'b9ca8ba5ee82fa0a1678f069'
db = SQLAlchemy(app)
from market import routes
