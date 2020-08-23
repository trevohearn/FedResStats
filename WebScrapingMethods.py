# Trevor O'Hearn
# 6/2/20
# Methods to help Scrape Fed Reserve

#imports
from bs4 import BeautifulSoup
import pandas as pd
import requests



#given dictionary, or month(s), day(s), year(s)
def getLinks(base_url, dates_dict=None, end_url_list = None, months=None, days=None, years=None):
    urls = []

    if (type(dates_dict) == dict):
        for d in dates_dict.keys():
            for v in dates_dict[d]:
                url = base_url + '2020{}{}/h41.htm'.format(d, v)
                urls.append(url)
        last = '{}/current/h41.htm'.format(base_url)
        urls.append(last)
    elif (months) and (days) and (years):
        for y in years:
            for m in months:
                for d in days:
                    url = base_url + '{}{}{}/h41.htm'.format(y, m, d)
                    urls.append(base_url)
        last = '{}/current/h41.htm'.format(base_url)
        urls.append(last)
    elif (months) and (days):
            for m in months:
                for d in days:
                    url = base_url + '{}{}{}/h41.htm'.format(y, m, d)
                    urls.append(base_url)
            last = '{}/current/h41.htm'.format(base_url)
            urls.append(last)
    elif (type(end_url_list) == list):
        for d in end_url_list:
            url = base_url + d
            urls.append(url)
    return urls

#returns beautifulsoup of html page
def getSoup(url):
    get = requests.get(url)
    return BeautifulSoup(get.content, 'html.parser')

#returns the feature names of the table
def getFeatures(bs):
    #identify what we want from each table
    dids = {}
    tables_bs = bs.select('table')
    maxtable = len(tables_bs)
    #starts at table 1 but tables_bs is 0 indexed
    curtable = int(tables_bs[0].find('th').attrs['id'].strip('t').split('r')[0])

    features = {}

    while curtable <= maxtable:
        #last table row
        #all data elements in row
        columns = len(tables_bs[curtable - 1].findAll('tr')[-1].findAll('td'))
        rows = len(tables_bs[curtable -1].findAll('tr'))
        dids[curtable] = []
        #get all features for table
        features[curtable] = tables_bs[curtable - 1].findAll('th', {'headers' : 't{}c0'.format(curtable)})
        rows = len(features[curtable])
        #go to next table
        curtable += 1
    return features

#add a way to select specific tables and break out of loop without breaking
def getData(features, bs, totaltablecols, tablecol):
    data = []
    tables = bs.select('table')
    i = 0
    #loop over all the tables
    for index, key in enumerate(features):
        #if table has features in it, get data
        if (len(features[key]) > 0):
            fs = features[key]
            #get all tds in table
            tds = tables[index].select('td')
            #loop over all features (rows) for table
            if (tablecol[i] == 'all'):
                #get all td data from table
                for td in tds:
                    data.append(td.text.strip())
            else:
                #get specific column of data
                for j, f in enumerate(fs):
                    spot = totaltablecols[i] * j + tablecol[i]
                    print(tds[spot])
                    thing = tds[spot].text.strip()
                    data.append(thing)

            #increment table parameters for next table
            i += 1
    return data

# def getTableData(features, bs, tablenum=1, column_num):
#     data = []
#     tables = bs.select('table')[tablenum]
#     for index, key in enumerate(features):
#         if (len(features[key]) > 0): #
#     return None

#strips the data and returns the chosen features
def cleanData(data, numFeatures, multiple=4, column=3, skip_amount=1, date_index=0):
    #skip date
    dataM = data[skip_amount:]
    dvals = {}
    dfvals = {'Date' : data[date_index].text.strip()}
    cleanData = [dfvals['Date']]
    for index in range(numFeatures):
        cleanData.append(dataM[multiple * index + column].text.strip())
    return cleanData


#clean features scraped from the web
#takes soup elements and returns dictionary of table and list of features
#skips empty soup elements
def cleanFeatures(features):
    cleaned_features = {}
    for key in features:
        cleaned_features[key] = []
        for value in features[key]:
            if (len(value.text) != 0): #not empty row
                cleaned_features[key].append(value.text.strip('\n !@#$%^&*()_'))
            else: #do nothing
                continue
    return cleaned_features


#returns the pandas dataframe from the given features and data
def createDataFrame(cleaned_features, data, date_index=0):
    #create df from cleaned_features
    print(len(cleaned_features), len(data))
    if (len(cleaned_features) != len(data)):
        return 'None'
    dvals = {}
    dfvals = {'Date' : data.pop(date_index).text.strip()}
    for key in data:
        dfvals[key] = data
    df = None
    try:
        df = pd.DataFrame(data=dfvals)
    except:
        df = pd.DataFrame(data=dfvals, index=[0])
    return df

#remove unic issues '\xa0'
def removeUnicode(x):
    if '\xa0' in str(x):
        return x.replace('\xa0', '')
    else:
        return x

#remove any +
def removePlus(x):
    if '+' in str(x):
        return x.replace('+', '')
    else:
        return x

#remove any ,
def removeComma(x):
    if ',' in str(x):
        return x.replace(',', '')
    else:
        return x

#remove any parentheses ()
def removeParentheses(x):
    if '(' in str(x):
        x = x.replace('(', '')
    if ')' in str(x):
        x = x.replace(')', '')
    else:
        return x
    return x

def removeAll(x):
    x = removeUnicode(x)
    x = removePlus(x)
    x = removeComma(x)
    x = removeParentheses(x)
    return x

# #given dataframe, features, and extras
# #return dateframe with unique columns
#
# def uniqueColumns(df, features, extras):
#     #pair similar extras to getFeatures
#     #consolodate extras from df and features from df
#     #check that features and extras are in df
#     all_cols = df.columns
#     #compare lists
#     if (features + extras == all_cols)
#         #good to go
#     else:
#         return 'not all columns accounted for'
#
#         pass
#         pass
#     return df
