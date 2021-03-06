from app import app, db
from app.models import Law, LawPart, LawSection, LawChapter, LawArticle
from bs4 import BeautifulSoup
import requests


def lvl_check( lvl, lvl_const ):
	is_null = 0

	if lvl < lvl_const:
		lvl_diff = lvl_const - lvl

		if lvl_diff == 1:
			print( ( '    ' * ( lvl_const - 1 ) ) + 'null' )
			lvl += 1
			is_null = 1

		elif lvl_diff == 2:
			print( ( '    ' * ( lvl_const - 2 ) ) + 'null' )
			print( ( '    ' * ( lvl_const - 1 ) ) + 'null' )
			lvl += 2
			is_null = 2

		elif lvl_diff == 3:
			print( ( '    ' * ( lvl_const - 3 ) ) + 'null' )
			print( ( '    ' * ( lvl_const - 2 ) ) + 'null' )
			print( ( '    ' * ( lvl_const - 1 ) ) + 'null' )
			lvl += 3
			is_null = 3

	elif lvl > lvl_const:
		lvl = lvl_const

	lvl += 1

	return lvl, is_null


array = [
	# { 'id': '28399',  'name': 'Конституция Российской Федерации' },
	#
	# { 'id': '37800',  'name': 'Арбитражный процессуальный кодекс Российской Федерации (АПК РФ)' },
	# { 'id': '19702',  'name': 'Бюджетный кодекс Российской Федерации (БК РФ)' },
	# { 'id': '60683',  'name': 'Водный кодекс Российской Федерации (ВК РФ)' },
	# { 'id': '13744',  'name': 'Воздушный кодекс Российской Федерации' },
	# { 'id': '51040',  'name': 'Градостроительный кодекс Российской Федерации' },
	# { 'id': '5142',   'name': 'Гражданский кодекс Российской Федерации - часть первая (ГК РФ ч. 1)' },
	# { 'id': '9027',   'name': 'Гражданский кодекс Российской Федерации - часть вторая (ГК РФ ч. 2)' },
	# { 'id': '34154',  'name': 'Гражданский кодекс Российской Федерации - часть третья (ГК РФ ч. 3)' },
	# { 'id': '64629',  'name': 'Гражданский кодекс Российской Федерации - часть четвертая (ГК РФ ч. 4)' },
	# { 'id': '39570',  'name': 'Гражданский процессуальный кодекс Российской Федерации (ГПК РФ)' },
	# { 'id': '51057',  'name': 'Жилищный кодекс Российской Федерации (ЖК РФ)' },
	# { 'id': '33773',  'name': 'Земельный кодекс Российской Федерации (ЗК РФ)' },
	# { 'id': '176147', 'name': 'Кодекс административного судопроизводства Российской Федерации (КАС РФ)' },
	# { 'id': '34661',  'name': 'Кодекс Российской Федерации об административных правонарушениях (КоАП)' },
	# { 'id': '64299',  'name': 'Лесной кодекс Российской Федерации (ЛК РФ)' },
	# { 'id': '19671',  'name': 'Налоговый кодекс Российской Федерации - часть первая (НК РФ ч. 1)' },
	# { 'id': '28165',  'name': 'Налоговый кодекс Российской Федерации - часть вторая (НК РФ ч. 2)' },
	# { 'id': '8982',   'name': 'Семейный кодекс Российской Федерации (СК РФ)' },
	# { 'id': '215315', 'name': 'Таможенный кодекс Евразийского экономического союза (ТК ЕАЭС)' },
	# { 'id': '34683',  'name': 'Трудовой кодекс Российской Федерации (ТК РФ)' },
	# { 'id': '12940',  'name': 'Уголовно-исполнительный кодекс Российской Федерации (УИК РФ)' },
	# { 'id': '34481',  'name': 'Уголовно-процессуальный кодекс Российской Федерации (УПК РФ)' },
	# { 'id': '10699',  'name': 'Уголовный кодекс Российской Федерации (УК РФ)' },
	#
	# { 'id': '305',    'name': 'Закон РФ "О защите прав потребителей" (ЗОЗПП) N 2300-1"' },
	# { 'id': '343',    'name': 'Закон РФ "О недрах" N 2395-1"' },
	# { 'id': '100',    'name': 'Закон РФ "О приватизации жилищного фонда в Российской Федерации" N 1541-1"' },
	# { 'id': '1511',   'name': 'Закон РФ "О средствах массовой информации" (о СМИ) N 2124-1"' },
	# { 'id': '5842',   'name': 'Федеральный закон "О банках и банковской деятельности" N 395-1"' },
	# { 'id': '121887', 'name': 'Федеральный закон "О бесплатной юридической помощи в Российской Федерации" N 324-ФЗ"' },
	# { 'id': '122855', 'name': 'Федеральный закон "О бухгалтерском учете" N 402-ФЗ"' },
	# { 'id': '45458',  'name': 'Федеральный закон "О валютном регулировании и валютном контроле" N 173-ФЗ"' },
	# { 'id': '22716',  'name': 'Федеральный закон "О ведомственной охране" N 77-ФЗ"' },
	# { 'id': '5490',   'name': 'Федеральный закон "О ветеранах" N 5-ФЗ"' },
	# { 'id': '116968', 'name': 'Федеральный закон "О внесении изменений в отдельные законодательные акты Российской Федерации в связи с совершенствованием принципов определения цен для целей налогообложения" N 227-ФЗ"' },
	# { 'id': '18260',  'name': 'Федеральный закон "О воинской обязанности и военной службе" N 53-ФЗ"' },
	# { 'id': '200506', 'name': 'Федеральный закон "О войсках национальной гвардии Российской Федерации" N 226-ФЗ"' },
	# { 'id': '32881',  'name': 'Федеральный закон "О государственной регистрации юридических лиц и индивидуальных предпринимателей" N 129-ФЗ"' },
	# { 'id': '182661', 'name': 'Федеральный закон "О государственной регистрации недвижимости" N 218-ФЗ"' },
	# { 'id': '304041', 'name': 'Федеральный закон "О государственной регистрации транспортных средств в Российской Федерации и о внесении изменений в отдельные законодательные акты Российской Федерации" N 283-ФЗ"' },
	# { 'id': '8368',   'name': 'Федеральный закон "О государственном регулировании производства и оборота этилового спирта, алкогольной и спиртосодержащей продукции и об ограничении потребления (распития) алкогольной продукции" N 171-ФЗ"' },
	# { 'id': '358750', 'name': 'Федеральный закон от 31.07.2020 N 248-ФЗ "О государственном контроле (надзоре) и муниципальном контроле в Российской Федерации"' },
	# { 'id': '6659',   'name': 'Федеральный закон "О государственных пособиях гражданам, имеющим детей" N 81-ФЗ"' },
	# { 'id': '36927',  'name': 'Федеральный закон "О гражданстве Российской Федерации" N 62-ФЗ"' },
	# { 'id': '286470', 'name': 'Федеральный закон "О ежемесячных выплатах семьям, имеющим детей" N 418-ФЗ"' },
	# { 'id': '54572',  'name': 'Федеральный закон "О концессионных соглашениях" N 115-ФЗ"' },
	# { 'id': '113658', 'name': 'Федеральный закон "О лицензировании отдельных видов деятельности" N 99-ФЗ"' },
	# { 'id': '8824',   'name': 'Федеральный закон "О некоммерческих организациях" N 7-ФЗ"' },
	# { 'id': '39331',  'name': 'Федеральный закон "О несостоятельности (банкротстве)" N 127-ФЗ"' },
	# { 'id': '61801',  'name': 'Федеральный закон "О персональных данных" N 152-ФЗ"' },
	# { 'id': '5438',   'name': 'Федеральный закон "О пожарной безопасности" N 69-ФЗ"' },
	# { 'id': '110165', 'name': 'Федеральный закон "О полиции" N 3-ФЗ"' },
	# { 'id': '37868',  'name': 'Федеральный закон "О правовом положении иностранных граждан в Российской Федерации" N 115-ФЗ"' },
	# { 'id': '262',    'name': 'Федеральный закон "О прокуратуре Российской Федерации" N 2202-1-ФЗ"' },
	# { 'id': '32834',  'name': 'Федеральный закон "О противодействии легализации (отмыванию) доходов, полученных преступным путем, и финансированию терроризма" N 115-ФЗ"' },
	# { 'id': '52144',  'name': 'Федеральный закон "О развитии малого и среднего предпринимательства в Российской Федерации" N 209-ФЗ"' },
	# { 'id': '54598',  'name': 'Федеральный закон "О контрактной системе в сфере закупок товаров, работ, услуг для обеспечения государственных и муниципальных нужд" N 44-ФЗ"' },
	# { 'id': '58968',  'name': 'Федеральный закон "О рекламе" N 38-ФЗ"' },
	# { 'id': '10148',  'name': 'Федеральный закон "О рынке ценных бумаг" N 39-ФЗ"' },
	# { 'id': '43224',  'name': 'Федеральный закон "О связи" N 126-ФЗ"' },
	# { 'id': '42413',  'name': 'Федеральный закон "О системе государственной службы Российской Федерации" N 58-ФЗ"' },
	# { 'id': '357765', 'name': 'Федеральный закон от 20.07.2020 N 211-ФЗ "О совершении финансовых сделок с использованием финансовой платформы"' },
	# { 'id': '181810', 'name': 'Федеральный закон "О стандартизации в Российской Федерации" N 162-ФЗ"' },
	# { 'id': '18853',  'name': 'Федеральный закон "О статусе военнослужащих" N 76-ФЗ"' },
	# { 'id': '164841', 'name': 'Федеральный закон "О стратегическом планировании в Российской Федерации" N 172-ФЗ"' },
	# { 'id': '45769',  'name': 'Федеральный закон "О страховании вкладов физических лиц в банках Российской Федерации" N 177-ФЗ"' },
	# { 'id': '15281',  'name': 'Федеральный закон "О судебных приставах" N 118-ФЗ"' },
	# { 'id': '107181', 'name': 'Федеральный закон "О таможенном регулировании в Российской Федерации" N 311-ФЗ"' },
	# { 'id': '304093', 'name': 'Федеральный закон "О таможенном регулировании в Российской Федерации и о внесении изменений в отдельные законодательные акты Российской Федерации" N 289-ФЗ"' },
	# { 'id': '115853', 'name': 'Федеральный закон "О техническом осмотре транспортных средств и о внесении изменений в отдельные законодательные акты Российской Федерации" N 170-ФЗ"' },
	# { 'id': '40241',  'name': 'Федеральный закон "О техническом регулировании" N 184-ФЗ"' },
	# { 'id': '34443',  'name': 'Федеральный закон "О трудовых пенсиях в Российской Федерации" N 173-ФЗ"' },
	# { 'id': '358753', 'name': 'Федеральный закон от 31.07.2020 N 259-ФЗ "О цифровых финансовых активах, цифровой валюте и о внесении изменений в отдельные законодательные акты Российской Федерации"' },
	# { 'id': '112702', 'name': 'Федеральный закон "Об административном надзоре за лицами, освобожденными из мест лишения свободы" N 64-ФЗ"' },
	# { 'id': '8743',   'name': 'Федеральный закон "Об акционерных обществах" (АО) N 208-ФЗ"' },
	# { 'id': '83311',  'name': 'Федеральный закон "Об аудиторской деятельности" N 307-ФЗ"' },
	# { 'id': '122222', 'name': 'Федеральный закон "Об инвестиционном товариществе" N 335-ФЗ"' },
	# { 'id': '19396',  'name': 'Федеральный закон "Об ипотеке (залоге недвижимости)" N 102-ФЗ"' },
	# { 'id': '71450',  'name': 'Федеральный закон "Об исполнительном производстве" N 229-ФЗ"' },
	# { 'id': '140174', 'name': 'Федеральный закон "Об образовании в Российской Федерации" N 273-ФЗ"' },
	# { 'id': '17819',  'name': 'Федеральный закон "Об обществах с ограниченной ответственностью" (ООО) N 14-ФЗ"' },
	# { 'id': '6693',   'name': 'Федеральный закон "Об общественных объединениях" N 82-ФЗ"' },
	# { 'id': '44571',  'name': 'Федеральный закон "Об общих принципах организации местного самоуправления в РФ" (закон о МСУ) N 131-ФЗ"' },
	# { 'id': '19559',  'name': 'Федеральный закон "Об обязательном социальном страховании от несчастных случаев на производстве и профессиональных заболеваний" N 125-ФЗ"' },
	# { 'id': '36528',  'name': 'Федеральный закон "Об обязательном страховании гражданской ответственности владельцев транспортных средств" (ОСАГО) N 40-ФЗ"' },
	# { 'id': '358670', 'name': 'Федеральный закон от 31.07.2020 N 247-ФЗ "Об обязательных требованиях в Российской Федерации"' },
	# { 'id': '12679',  'name': 'Федеральный закон "Об оружии" N 150-ФЗ"' },
	# { 'id': '121895', 'name': 'Федеральный закон "Об основах охраны здоровья граждан в Российской Федерации" N 323-ФЗ"' },
	# { 'id': '199976', 'name': 'Федеральный закон "Об основах системы профилактики правонарушений в Российской Федерации" N 182-ФЗ"' },
	# { 'id': '366141', 'name': 'Федеральный закон от 01.04.2020 N 104-ФЗ (ред. от 27.10.2020) "Об особенностях исчисления пособий по временной нетрудоспособности и осуществления ежемесячных выплат в связи с рождением (усыновлением) первого или второго ребенка"' },
	# { 'id': '314646', 'name': 'Федеральный закон "Об ответственном обращении с животными и о внесении изменений в отдельные законодательные акты Российской Федерации" N 498-ФЗ"' },
	# { 'id': '34823',  'name': 'Федеральный закон "Об охране окружающей среды" N 7-ФЗ"' },
	# { 'id': '314643', 'name': 'Федеральный закон "Об уполномоченных по правам ребенка в Российской Федерации" N 501-ФЗ"' },
	# { 'id': '358738', 'name': 'Федеральный закон от 31.07.2020 N 258-ФЗ "Об экспериментальных правовых режимах в сфере цифровых инноваций в Российской Федерации"' },
	# { 'id': '366950', 'name': 'Федеральный конституционный закон от 06.11.2020 N 4-ФКЗ "О Правительстве Российской Федерации"' },
]


for arr in array:

	url = "http://www.consultant.ru/document/cons_doc_LAW_" + arr['id'] + "/"
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'}

	soup    = BeautifulSoup( requests.get(url, headers = headers).text, 'lxml')
	content = soup.find("contents")
	links   = content.find_all("a")

	law = Law( title = arr['name'] )
	db.session.add( law )
	db.session.commit()

	lid_law = law.id

	print()
	print(f'======= {arr["name"]} =======')
	print()

	lvl = 0

	lid_part = 0
	lid_section = 0
	lid_chapter = 0

	for link in links:

		if link.text[0] == 'Ч':
			lvl, is_null = lvl_check(lvl, 0)

			last_part = LawPart( id_law = lid_law, title = link.text )
			db.session.add( last_part )
			db.session.commit()

			lid_part = last_part.id

			print( link.text )

		if link.text[0] == 'Р':
			lvl, is_null = lvl_check(lvl, 1)

			if is_null == 1:
				last_part = LawPart( id_law = lid_law, title = None )
				db.session.add( last_part )
				db.session.commit()

				lid_part = last_part.id

			last_section = LawSection( id_part = lid_part, name = link.text )
			db.session.add( last_section )
			db.session.commit()

			lid_section = last_section.id

			print( '    ' + link.text )

		if link.text[0] == 'Г':
			lvl, is_null = lvl_check(lvl, 2)

			if is_null == 1:
				last_section = LawSection( id_part = lid_part, name = None )
				db.session.add( last_section )
				db.session.commit()

				lid_section = last_section.id

			if is_null == 2:
				last_part = LawPart( id_law = lid_law, title = None )
				db.session.add( last_part )
				db.session.commit()

				lid_part = last_part.id

				last_section = LawSection( id_part = lid_part, name = None )
				db.session.add( last_section )
				db.session.commit()

				lid_section = last_section.id

			last_chapter = LawChapter( id_section = lid_section, name = link.text[:500] )
			db.session.add( last_chapter )
			db.session.commit()

			lid_chapter = last_chapter.id

			print( '        ' + link.text )

		if link.text[0] == 'С':
			lvl, is_null = lvl_check(lvl, 3)

			if is_null == 1:
				last_chapter = LawChapter( id_section = lid_section, name = None )
				db.session.add( last_chapter )
				db.session.commit()

				lid_chapter = last_chapter.id

			if is_null == 2:
				last_section = LawSection( id_part = lid_part, name = None )
				db.session.add( last_section )
				db.session.commit()

				lid_section = last_section.id

				last_chapter = LawChapter( id_section = lid_section, name = None )
				db.session.add( last_chapter )
				db.session.commit()

				lid_chapter = last_chapter.id

			if is_null == 3:
				last_part = LawPart( id_law = lid_law, title = None )
				db.session.add( last_part )
				db.session.commit()

				lid_part = last_part.id

				last_section = LawSection( id_part = lid_part, name = None )
				db.session.add( last_section )
				db.session.commit()

				lid_section = last_section.id

				last_chapter = LawChapter( id_section = lid_section, name = None )
				db.session.add( last_chapter )
				db.session.commit()

				lid_chapter = last_chapter.id

			page_link = "http://www.consultant.ru" + link['href']

			page = BeautifulSoup( requests.get(page_link, headers = headers).text, 'lxml')
			text = page.select_one(".document .text")

			try:
				text.find('h1').decompose()
			except:
				pass

			try:
				for div in text.select('.C'):
					div.decompose()
			except:
				pass

			try:
				for div in text.select('.L'):
					div.decompose()
			except:
				pass

			spans = text.find_all('span')

			data = ""

			for span in spans:
				data += "<p>" + span.text + "</p>"

			last_article = LawArticle( id_chapter = lid_chapter, name = link.text, text = data )
			db.session.add( last_article )
			db.session.commit()

			print( '            ' + link.text )
