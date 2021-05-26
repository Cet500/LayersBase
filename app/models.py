from app import db


class Law(db.Model):
	# Закон
	id    = db.Column( db.Integer, primary_key = True )
	title = db.Column( db.String(512), index = True, nullable = False )

	parts = db.relationship( "LawPart", backref = "parts", lazy = "dynamic" )

	def __repr__(self):
		return f'<law {self.id}>'


class LawPart(db.Model):
	# Часть
	id     = db.Column( db.Integer, primary_key = True )
	id_law = db.Column( db.Integer, db.ForeignKey( 'law.id' ), nullable = False )
	title  = db.Column( db.String(512), index = True, nullable = True )

	sections = db.relationship( 'LawSection', backref = "sections", lazy = "dynamic" )

	def __repr__(self):
		return f'<part {self.id} of law {self.id_law}>'


class LawSection(db.Model):
	# Раздел
	id      = db.Column( db.Integer, primary_key = True )
	id_part = db.Column( db.Integer, db.ForeignKey( 'law_part.id' ), nullable = False )
	name    = db.Column( db.String(512), index = True, nullable = True )

	chapters = db.relationship( 'LawChapter', backref = "chapters", lazy = "dynamic" )

	def __repr__(self):
		return f'section {self.id} of part {self.id_law}'


class LawChapter(db.Model):
	# Глава
	id         = db.Column( db.Integer, primary_key = True )
	id_section = db.Column( db.Integer, db.ForeignKey( 'law_section.id' ), nullable = False )
	name       = db.Column( db.String(512), index = True, nullable = True )

	articles = db.relationship( 'LawArticle', backref = "articles", lazy = "dynamic" )

	def __repr__(self):
		return f'chapter {self.id} of section {self.id_section}'


class LawArticle(db.Model):
	# Статья
	id         = db.Column( db.Integer, primary_key = True )
	id_chapter = db.Column( db.Integer, db.ForeignKey( 'law_chapter.id' ), nullable = False )
	name       = db.Column( db.String(1024), nullable = True )
	text       = db.Column( db.Text(65000), nullable = False )

	def __repr__(self):
		return f'article {self.id} of chapter {self.id_chapter}'
