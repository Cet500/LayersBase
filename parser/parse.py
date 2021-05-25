from bs4 import BeautifulSoup
import requests


def lvl_check( lvl, lvl_const ):
	if lvl < lvl_const:
		lvl_diff = lvl_const - lvl
		if lvl_diff == 1:
			print( ( '    ' * ( lvl_const - 1 ) ) + 'null' )
		elif lvl_diff == 2:
			print( ( '    ' * ( lvl_const - 2 ) ) + 'null' )
			print( ( '    ' * ( lvl_const - 1 ) ) + 'null' )
		elif lvl_diff == 3:
			print( ( '    ' * ( lvl_const - 3 ) ) + 'null' )
			print( ( '    ' * ( lvl_const - 2 ) ) + 'null' )
			print( ( '    ' * ( lvl_const - 1 ) ) + 'null' )
		lvl += 1

	elif lvl > lvl_const:
		lvl = lvl_const

	lvl += 1

	return lvl


url = "http://www.consultant.ru/document/cons_doc_LAW_34481/"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'}

soup    = BeautifulSoup( requests.get(url, headers = headers).text, 'lxml')
content = soup.find("contents")
links   = content.find_all("a")

lvl = 0

for link in links:
	if link.text[0] == 'Ч':
		lvl = lvl_check(lvl, 0)
		print( link.text )

	elif link.text[0] == 'Р':
		lvl = lvl_check(lvl, 1)
		print( '    ' + link.text )

	elif link.text[0] == 'Г':
		lvl = lvl_check(lvl, 2)
		print( '        ' + link.text )

	elif link.text[0] == '§':
		lvl = lvl_check(lvl, 3)
		print( '            ' + link.text )

	elif link.text[0] == 'С':
		lvl = lvl_check(lvl, 4)
		print( '                ' + link.text )
