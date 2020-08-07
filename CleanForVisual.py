#Trevor O'Hearn
#9/7/20
# Place to clean dataframe for plotly visuals

import pandas as pd
import plotly.express as px

df = pd.read_csv('fedreservesummary.csv')
df.set_index('Date', inplace=True)



#create figure
import plotly.express as px
#fig = px.pie(df, values='tip', names='day', color_discrete_sequence=px.colors.sequential.RdBu
fig = px.pie(df.iloc[21], names = df.columns, values = vals,
             color_discrete_sequence=px.colors.sequential.RdBu,
            title = 'Use of Federal Reserve Funds (>1% of assets)')
