# Author: https://github.com/Khisrav/
# This scripts downloads manga from mangafast.net
# Just run script and past link to the manga (like https://mangafast.net/read/{MANGA_NAME}) into appeared window 
from bs4 import BeautifulSoup
import requests
import urllib
import os.path
print('Enter the URL of manga from mangafast.net')
URL = input()
print('Started')
page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')
print('Getting page')
title_soup = soup.find('title')
title = title_soup.text
if os.path.isdir(title) == False:
	os.mkdir(title)
all_links = soup.find_all('a', class_='chapter-link', href=True, title=True)
print('Parsing chapters list')
chapters_url = []
chapters_title = []
for a in all_links:
	chapters_url.append(a['href'])
	chapters_title.append(a['title'])
chapters_url.pop(0)
chapters_url.reverse()
chapters_title.pop(0)
chapters_title.reverse()
index = 0
print('Downloading...')
for chapter_url in chapters_url:
	chapter_title = chapters_title[index]
	chapter_page = requests.get(chapter_url)
	chapter_soup = BeautifulSoup(chapter_page.text, 'html.parser')
	chapter_html_container = chapter_soup.find('div', class_='content-comic')
	chapter_images = chapter_html_container.findChildren('img')
	for image in chapter_images:
		if os.path.exists(title+'/'+chapter_title) == False:
			os.mkdir(title+'/'+chapter_title)
		if (os.path.exists(title+'/'+chapter_title+'/'+str(image['alt'])+'.png')) == False:
			urllib.request.urlretrieve(image['src'], title+'/'+chapter_title+'/'+str(image['alt'])+'.png')
	index+=1
	print(str(chapter_title) + ' is downloaded.')
print('Completed')