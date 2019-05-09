from bs4 import BeautifulSoup
import re
import requests
import os, sys

save_path = 'D:\\gern\\Desktop\\Prog\\Python\\scraper\\books'

# set up; get url and parse to the relevant table
data = requests.get('https://en.uesp.net/wiki/Skyrim:Books#All_Books')
soup = BeautifulSoup(data.text, 'html.parser')
table = soup.find(text='Hircine\'s Tale').find_parent('table')

# get all titles, which are all bolded
title = [t.text for t in table.find_all('b')]

# get all title links
links = []
for book in table.find_all('a', href=True):
    if book.text in title:
        links.append(book['href'].strip('/wiki/Skyrim:'))

i = 0
# for link in links:
#     if i == 3:
#         sys.exit()
#     data = requests.get('https://en.uesp.net' + link)
#     soup = BeautifulSoup(data.text, 'html.parser')
#     content = soup.find('div', class_='book')
#     comp = os.path.join(save_path, title[i] + '.html')
#     with open(comp, 'w', encoding='utf-8') as f:
#         f.write(content.prettify())
#     i+=1


# debug
comp = os.path.join(save_path, 'out.txt')
with open(comp, 'w', encoding='utf-8') as f:
    for t in links: f.write(t +'\n') 
