#Trevor O'Hearn
#6/1/2020
#WebScraping.py
#Scrapes values from fed reserve weekly summary statement

import requests
from bs4 import BeautifulSoup

url = 'https://www.federalreserve.gov/releases/h41/current/h41.htm'
get = requests.get(url)
bs = BeautifulSoup(get.content, 'html-parser')

data = bs.select('.H41Release > tr > td > p')
