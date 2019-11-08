from bs4 import BeautifulSoup
import requests
import re

index_page = requests.get("https://www.biblestudytools.com/dictionaries/eastons-bible-dictionary/")
soup = BeautifulSoup(index_page.content, 'lxml')
index_links = soup.select(".row > .col-xs-12 > ul.nav.nav-tabs.nav-tabs-justified")[0].find_all('a', attrs={'class': None})
f= open("easton_bible_entries2.txt","w+")
for i in range(0,len(index_links)):
	letter_index_page = requests.get(index_links[i]['href'])
	soup = BeautifulSoup(letter_index_page.content, 'lxml')
	letter_index_links = 1
	entries = soup.select('div.col-md-6 > ul.list-group.bst-list-group')[1].find_all('a', attrs={'class': None})

	for entry in entries:
		entry_page = requests.get(entry['href'])
		soup = BeautifulSoup(entry_page.content, 'lxml')
		entry_content = soup.select('.library')[0]

		if len(entry_content.contents) > 1:
			entry_content = str(entry_content)
			entry_content = re.sub(r'<a.*?>', '', entry_content)
			entry_content = re.sub(r'</a>', '', entry_content)
			entry_content = re.sub(r'<font.*?>.*?</font>', '', entry_content)
			entry_content = re.sub(r'<hr.*?/>', '', entry_content)
			entry_content = re.sub(r'<p> </p>', '', entry_content)
			entry_content = re.sub(r'<center></center>', '', entry_content)
			entry_content = re.sub(r'</article>', '', entry_content)
			entry_content = entry_content.replace('\n', ' ').replace('\r', '').replace('\t', '')
			content = str(entry_content).strip()
			title = str(entry.text).strip()
			f.write("%s\t%s\n" % (title, content))
f.close()