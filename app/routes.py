from flask import render_template, url_for
from app import app, db

# ------------------------ main pages ------------------------ #

@app.route('/')
@app.route('/index')
def index():
	return "Hello World!"
