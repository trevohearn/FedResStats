#Trevor O'Hearn
#6/1/2020
#WebScraping.py
#Scrapes values from fed reserve weekly summary statement

import requests
from bs4 import BeautifulSoup
import WebScrapingMethods as wsm
import pandas as pd


base_url = 'https://www.federalreserve.gov/releases/h41/'
#get = requests.get(url)
#bs = BeautifulSoup(get.content, 'html-parser')

#data = bs.select('.H41Release > tr > td > p')

# dates = {'01' : ['02', '09','16','23','30'],
#         '02' : ['06', '13', '20' , '27'],
#         '03' : ['05', '12', '19' , '26'],
#         '04' : ['02', '09', '16', '23', '30'],
#          '05' : ['07', '14', '21'] #has current
#         }

#get list for links
soup = wsm.getSoup(base_url)
hrefs = soup.select('.col-xs-1 a')
end_urls = []
for a in hrefs:
    end_urls.append(a.attrs['href'] + '/h41.htm')

urls = wsm.getLinks(base_url, end_url_list=end_urls)
dfs = []
for url in urls:
    print(url)
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
    #print(clean_features)
    #print(clean_data)
    dfs.append(wsm.createDataFrame(clean_features, clean_data))
#print(type(dfs[0]))

df = dfs[0]
for d in dfs[1:]:
    df = df.append(d, ignore_index=False)
df['Date'] = pd.to_datetime(df['Date'], format='%B %d, %Y', errors='ignore')
df.set_index('Date', inplace=True)

all_dfs = [df]
columnNames = df.columns
df.fillna('0', inplace=True)
#clean data frame
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
#make way to consolodate duplicate columns
#add banks and such
df.to_csv('fedreservesummary_test.csv')
