from flask import render_template, url_for, request, send_from_directory
from app import app, db
from app.models import Law, LawPart, LawSection, LawChapter, LawArticle

# ------------------------ main pages ------------------------ #

@app.route('/')
@app.route('/index')
def index():
	laws = Law.query.order_by(Law.id).all()

	return render_template( "index.html", title = "Главная", laws = laws )


@app.route('/find')
def find():
	query        = request.args.get('query', type = str)
	query_err    = None
	res_names    = None
	res_chapters = None
	res_articles = None

	if len(query) < 3:
		query_err = 'Слишком короткий запрос'
	else:
		res_names    = Law.query.filter( Law.title.like(f'%{query}%') )
		res_chapters = LawChapter.query.filter( LawChapter.name.like(f'%{query}%') )
		res_articles = LawArticle.query.filter( LawArticle.name.like(f'%{query}%') )

	return render_template( "find.html", title = "Главная", query = query, query_err = query_err, res_names = res_names,
	                                     res_chapters = res_chapters, res_articles = res_articles )


@app.route('/full/<int:id>')
def full(id):
	law = Law.query.get(id)

	return render_template( "full.html", title = law.title, law = law )


@app.route('/law/<int:id>')
def law(id):
	law = Law.query.get(id)

	return render_template( "law.html", title = law.title, law = law )


@app.route('/part/<int:id>')
def part(id):
	part = LawPart.query.get( id )
	law  = Law.query.get( part.id_law )

	return render_template( "part.html", title = part.title, part = part, law = law )


@app.route('/section/<int:id>')
def section(id):
	section = LawSection.query.get( id )
	part    = LawPart.query.get( section.id_part )
	law     = Law.query.get( part.id_law )

	return render_template( "section.html", title = section.name, section = section, part = part, law = law )


@app.route('/chapter/<int:id>')
def chapter(id):
	chapter = LawChapter.query.get( id )
	section = LawSection.query.get( chapter.id_section )
	part    = LawPart.query.get( section.id_part )
	law     = Law.query.get( part.id_law )

	return render_template( "chapter.html", title = chapter.name, chapter = chapter, section = section, part = part,
	                                        law = law )


@app.route('/article/<int:id>')
def article(id):
	article = LawArticle.query.get( id )
	chapter = LawChapter.query.get( article.id_chapter )
	section = LawSection.query.get( chapter.id_section )
	part    = LawPart.query.get( section.id_part )
	law     = Law.query.get( part.id_law )

	return render_template( "article.html", title = article.name, article = article, chapter = chapter, section = section,
	                                        part = part, law = law )

# ------------------------ technical pages ------------------------ #


@app.route('/favicon.ico')
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
	return send_from_directory(app.static_folder, request.path[1:])
