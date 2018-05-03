import requests
from bs4 import BeautifulSoup

url = 'https://ev-database.uk'
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'lxml')

urls = []
for h in soup.find_all('h2'):
    a = h.find('a')
    urls.append(a.attrs['href'])
    

import requests 
import pandas as pd

# TO DO: create a for - loop for iterating through the url-list 
list_length = len(urls)

#loop takes about 10 minutes


for x in range(list_length):
    page_link ='https://ev-database.uk' + urls[x]
    tabelle = pd.read_html(requests.get(page_link).content)[1]
    for i in range(2,18):
        tabelleNext = pd.read_html(requests.get(page_link).content)[i]
        tabelle = tabelle.append(tabelleNext, ignore_index = True)
