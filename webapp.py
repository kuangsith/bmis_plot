import pandas as pd
import datetime
import datalib
import streamlit as st
import numpy


st.header('BMIS DATA')


with st.expander("Setting"):
    st.write(f"Will add things here")

js = datalib.get_since_long('2024-02-15','2024-02-18')
datalib.process_json(js)
df = datalib.processed_json_to_df(js)

st.line_chart(data=df,x='time',y='WaterTemp_ACTW')



