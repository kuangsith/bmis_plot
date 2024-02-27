import pandas as pd
from bs4 import BeautifulSoup
import requests
import streamlit as st
import numpy
import config
import pandas as pd
import time
from bokeh.plotting import figure

st.header('BIMS DATA')

npoints = 60*24*3
samplerate = 1

tablist = config.tablist()
unit_dict = config.unit_dict()

with st.expander("Setting"):
    st.write(f"Table name and column name will be selected here")
    tabname = st.radio("Select table name:",tablist,captions=tablist)

start = time.time()

url = f'http://110.49.150.135:4002/CPU/?command=DataQuery&uri=dl:tab{tabname}&format=html&mode=most-recent&p1={npoints}&p2='
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

table = soup.find('table')
rows = table.find_all('tr')

data = []
for row in rows:
    cols = row.find_all(['td', 'th'])
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

df = pd.DataFrame(data[1:],columns=data[0])

collist= [col for col in df.columns if col not in ['TimeStamp','Record']]

df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])
for col in collist:
    df[col] = df[col].astype('float')
    


df_lite = df[(df.index % samplerate) == 0].copy().reset_index(drop=True)

# for col in collist:
#     # print(col)
#     st.line_chart(data=df_lite,x='TimeStamp',y=col,height=400)

for col in collist:
    p = figure(
    title=col,
    x_axis_label='Time',
    y_axis_label= unit_dict.get(col) if unit_dict.get(col) is not None else col,
    x_axis_type="datetime")

    p.line(df_lite['TimeStamp'], df_lite[col], line_width=2)
    st.bokeh_chart(p, use_container_width=True)


end = time.time()

st.write(f'Time spent: {round(end-start,2)} seconds based on last {npoints} data points, sample rate = 1 in {samplerate}.')
