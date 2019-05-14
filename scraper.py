from bs4 import BeautifulSoup
import requests, re
import os, sys
import zipfile

# epub from html
# http://www.manuel-strehl.de/dev/simple_epub_ebooks_with_python.en.html

save_path = 'books'
if not os.path.exists(save_path):
    os.makedirs(save_path)

# set up; get url and parse to the relevant table
data = requests.get('https://en.uesp.net/wiki/Skyrim:Books#All_Books')
soup = BeautifulSoup(data.text, 'html.parser')
table = soup.find(text='Hircine\'s Tale').find_parent('table')

# get all titles, which are all bolded
title = [t.text for t in table.find_all('b')]

# get all title links
# 469 BOOKS OVERALL
links = []
for book in table.find_all('a', href=True):
    if book.text in title:
        links.append(book['href'].strip('/wiki/Skyrim:'))

# page_source = 'https://en.uesp.net/wiki/Skyrim:'
page_source = 'https://skyrim.gamepedia.com/'	

manifest = ""
spine = ""

# index file that lists all other html files
containerXML = '''<container version="1.0"
           xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/Content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>'''

# another xml file, living per convention in OEBPS/content.xml
index_tpl = '''<package version="2.0"
  xmlns="http://www.idpf.org/2007/opf">
  <metadata/>
  <manifest>
	%(manifest)s
  </manifest>
  <spine toc="ncx">
	%(spine)s
  </spine>
</package>'''

def writeHTML(file_name, i):
	# copy opening line then write content to html	
	data = requests.get(page_source + links[i])
	soup = BeautifulSoup(data.text, 'html.parser')
	content = soup.find('blockquote')
	
	line = '''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title></title>
</head>
<body>
'''
	
	if not content is None:
		with open(file_name, 'w') as e:
			e.write(line)
			for p in content.find_all('p'): 
				e.write(p.prettify())
			e.write("</body>\n</html>")
		return True
	return False

# making each epub	
for i in range(4,10):
	# create HTML content for epub
	html_basename = os.path.join(save_path, title[i] + '.html');
	html_is_available = writeHTML(html_basename, i)
	
	if html_is_available:
		# main file of epub
		saved_file = os.path.join(save_path, title[i] + '.epub');
		epub = zipfile.ZipFile(saved_file, 'w')
		
		# first file is "mimetype"
		epub.writestr('mimetype', 'application/epub+zip')
		
		# this is referenced in META_INF/container.xml
		epub.writestr("META-INF/container.xml", containerXML);
		
		# link html in content.opf
		manifest = '<item id="file_%s" href="%s" media-type="application/xhtml+xml"/>' % (
					  1, 'content.html')
		spine = '<itemref idref="file_%s" />' % (1)
		epub.write(html_basename, 'OEBPS/content.html')
		
		epub.writestr('OEBPS/Content.opf', index_tpl % {
		  'manifest': manifest,
		  'spine': spine,
		})
			


# debug
# comp = os.path.join(save_path, 'out.txt')
# with open(comp, 'w', encoding='utf-8') as f:
    # for t in links: f.write(t +'\n') 