# Federal Reserve Statistical Release Project
The Federal Reserve sends out detailed reports every week about what they are doing with the nation's money. The webpage itself is nothing special, and mostly just a large pile of text. I decided to scrape the valuable information from each document and try to represent it in a more appealing way.

Right now, I have two .csv files that are from the first overview table of the report and the second is specifically about what each bank is doing. Also go ahead and check out banksgraph.html, it is an interactive line graph using plotly showing each bank's total assets.

## Pie-Chart of Distribution
!['Plotly Pie Chart'](https://github.com/trevohearn/FedResStats/blob/master/images/PlotlyPieChart.png)

## Line Graph of Rolling Totals
!['Plotly Line Chart'](https://github.com/trevohearn/FedResStats/blob/master/images/TotalFedResLineChart.png)

## Banks Assets Overview
!['Banks Line Chart'](https://github.com/trevohearn/FedResStats/blobl/master/images/BanksAssetsOverview.png)

## Goal
- To use data visualization to better explain what the government spends the nation's money on
- To use webscraping to automatically gather the new data every week and make it easily manipulatable and readily available

## Process
- Use BeautifulSoup to automatically scrape the federalreserve.gov website for the weekly statistical Release
- Clean the data and add it to a dataframe using Pandas
- Visualize the data using Plotly

## In progress
- Automating the process through WebScraping.py (The main .csv file of data was pulled using Jupyter Notebook)
- Scraping more than just the first table in the Federal Reserve Summary

## Future
- Add more visuals and data analysis
- Create Frontend to select tables, sort by data and choose visuals
- Go back to all readily available data (June 1996)
