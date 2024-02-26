#!/usr/bin/python3
""" Market python file"""

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/about/<username>')
def about_page(username):
    return f'<h1>this is the about page for {username}<h1>'
