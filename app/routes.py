from flask import render_template, url_for, request, send_from_directory
from app import app, db
from app.models import Law

# ------------------------ main pages ------------------------ #

@app.route('/')
@app.route('/index')
def index():
	laws = Law.query.order_by(Law.id).all()

	return render_template( "index.html", title = "Главная", laws = laws )


# ------------------------ technical pages ------------------------ #


@app.route('/favicon.ico')
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
	return send_from_directory(app.static_folder, request.path[1:])
