#Trevor O'Hearn
#8/4/20
#Written to Quickly Scrape the overview table of the Federal Reserve

import pandas as pd
import requests
from bs4 import BeautifulSoup
import WebScrapingMethods as wsm

base_url = 'https://www.federalreserve.gov/releases/h41/'

#get list for links
soup = wsm.getSoup(base_url)
hrefs = soup.select('.col-xs-1 a')
end_urls = []
for a in hrefs:
    #get links for 2020 and 2019
    if (a.attrs['href'][:4] == '2020' or a.attrs['href'][:4] == '2019'
        or a.attrs['href'][:4] == 'curr'):
        end_urls.append(a.attrs['href'] + '/h41.htm')
    else:
        break

urls = wsm.getLinks(base_url, end_url_list=end_urls)
dfs = []
for url in urls:
    bs = wsm.getSoup(url)
    date = bs.select('.H41Release td p')[0].text.strip()
    print(date)
    features = wsm.getFeatures(bs)
    table = bs.select('table')[1]
    tds = table.select('td')
    data = []
    i = 0
    while i < (len(tds) / 4):
        text = tds[4 * i + 3].text.strip()
        if (len(text) > 0):
            data.append(text)
        i += 1
    cleaned_features = wsm.cleanFeatures(features)

    dfvals = {}
    dfvals['Date'] = date
    for i, f in enumerate(cleaned_features[2]):
        dfvals[f] = data[i]

    df = pd.DataFrame(data=dfvals, index=[0])
    dfs.append(df)

#clean dataframe
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
        df[c] = df[c].apply(wsm.removeUnicode)
        df[c] = df[c].apply(wsm.removePlus)
        df[c] = df[c].apply(wsm.removeComma)
        df[c] = df[c].astype(int)
        #df[c] = df[c].apply(wsm.removeAll)
all_dfs[0].to_csv('FederalReserveSummaryAugust4th2020.csv')

#import pickle as p
#p.save()
#p.loda()
