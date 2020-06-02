#Trevor O'Hearn
#6/1/2020
#WebScraping.py
#Scrapes values from fed reserve weekly summary statement

import requests
from bs4 import BeautifulSoup
import WebScrapingMethods as wsm
import pandas as pd


base_url = 'https://www.federalreserve.gov/releases/h41/'
get = requests.get(url)
bs = BeautifulSoup(get.content, 'html-parser')

data = bs.select('.H41Release > tr > td > p')

dates = {'01' : ['02', '09','16','23','30'],
        '02' : ['06', '13', '20' , '27'],
        '03' : ['05', '12', '19' , '26'],
        '04' : ['02', '09', '16', '23', '30'],
         '05' : ['07', '14', '21'] #has current
        }

urls = wsm.getLinks(base_url, dates_dict=dates)

dfs = []
for url in urls:
    bs = wsm.getSoup(url)
        data = bs.select('.H41Release > tr > td > p')
    if (len(data) == 0):
        data = bs.select('.H41Release td p')
        if (len(data) == 0):
            print('no data')
            print(url)
            break;
    features = wsm.getFeatures(bs)
    clean_features = wsm.cleanFeatures(features)
    clean_data = wsm.cleanData(data, len(clean_features[2]))
    dfs.append(wsm.createDataFrame(clean_features, clean_data))
df = dfs[0]
for d in dfs[1:]:
    df = df.append(d, ignore_index=False)
df['Date'] = pd.to_datetime(df['Date'], format='%B %d, %Y', errors='ignore')
df.set_index('Date', inplace=True)

all_dfs = [df]
columnNames = df.columns
df.fillna('0', inplace=True)
for df in all_dfs:
    for c in columnNames:
        df[c] = df[c].apply(removeUnicode)
        df[c] = df[c].apply(removePlus)
        df[c] = df[c].apply(removeComma)
        df[c] = df[c].astype(int)
#pd.to_datetime('13000101', format='%Y%m%d', errors='coerce')
#rename df
namesdict = {}
for i, c in enumerate(df.columns):
    namesdict[c] = c.strip('1234567890').title()
df.rename(namesdict, axis='columns', inplace=True)
