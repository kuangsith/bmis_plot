import pandas as pd
import datetime
import datalib
import streamlit as st
import numpy


st.header('BMIS DATA')


with st.expander("Setting"):
    st.write(f"Table name and column name will be selected here")

js = datalib.get_since_long('2024-02-15','2024-02-18')
datalib.process_json(js)
df = datalib.processed_json_to_df(js)


collist= [col for col in df.columns if col not in ['time','no']]

for col in collist:
    st.line_chart(data=df,x='time',y=col)



