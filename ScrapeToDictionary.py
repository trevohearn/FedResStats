# Trevor O'Hearn
# 8/23/2020
# ScrapeToDictionary.py
# Scrapes the Federal Reserve and converts the data from the tables into a
# dictionary that is then written into a pickled file to be used by other programmers
# Dependencies :
# BeautifulSoup, WebScrapingMethods, pickle

import pandas as pd
import requests
from bs4 import BeautifulSoup
import WebScrapingMethods as wsm
import pickle as p

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

dated_all_tables = {}
for url in urls:
    bs = wsm.getSoup(url)
    date = bs.select('.H41Release td p')[0].text.strip()
    table_columns = []
    table_rows = []
    table_data = {}
    features = wsm.cleanFeatures(wsm.getFeatures(bs))
    k = 0
    failures = []
    for table in tables:
        #get dimensions of table
        try:

            k += 1
            flag = 0
            if (table.select('th', limit=1)[0].attrs['id'].split('c')[1] == '0'):
#                print('actually a table: {}'.format(table.select('th', limit=1)[0].text))
                flag = 1
            across = len(table.select('tr')[-1].select('p')) - 1 #can't count the header column
            down = len(table.select('td')) // across
            bank_bool = False
            if (across > 10): #table of banks
                bank_bool = True
            table_columns.append(across)
            table_rows.append(down)

            #get features
            table_num = int(table.select('tr th', limit=1)[0].attrs['id'].strip('t').split('c')[0])
            features[table_num]
            flag = 2
            #get data
            tds = table.select('td')
            data = []
            i = 0
            while i < down:
                text = None
                if (bank_bool): #total is in first column
                    text = tds[across * i].text.strip()
                else: #total is last column
                    text = tds[across * i + across - 1].text.strip()
                if (len(text) > 0):
                    data.append(text)
                i += 1
            table_data[table_num] = dict(zip(features[table_num], data))
            flag = 3
#            print('zipped : {}, {}'.format(table_num, flag))
        except:
#            print(flag)
            failures.append(k)
            continue
#    print(failures)
    #supposed to fail : 0,3,5, 7, 9, 11, 14, 17, 19 (0 indexed)

    #take dictionaries of tables and make a singulare dictionary
    all_tables_data = {}
    for key in table_data:
        for k in table_data[key]:
            if k in all_tables_data.keys(): #key name already exists
                all_tables_data['{} in {}'.format(k, key)] = table_data[key][k]
            else:
                all_tables_data[k] = table_data[key][k]
    for k in table_data:
        for key in table_data[k]:
            val = table_data[k][key]
            val = wsm.removeUnicode(val)
            val = wsm.removePlus(val)
            val = wsm.removeComma(val)
            val = wsm.removeParentheses(val)
            try:
                val = int(val)
            except:
                continue
            table_data[k][key] = val
    dated_all_tables[date] = all_tables_data
    print(date)
    #take singular dictionary and create dataframe
    #df = pd.DataFrame(data=all_tables_data, index=[0])


p,dump( dated_all_tables, open('dates_all_tables.p', 'wb'))

#to load
#p.load( open( "dated_all_tables.p", "rb" ) )
