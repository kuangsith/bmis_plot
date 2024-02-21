import requests
import datetime
import pandas as pd
from matplotlib import pyplot as plt

table_list = ['ACTW','ACLW ','AROW']
unitdict = {'WaterTemp_ACTW':'°C'}

def fetch_api_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4XX and 5XX status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None

def get_recent(tbname=table_list[0]):
    api_url = f"http://110.49.150.135:4002/CPU/?command=DataQuery&uri=dl:tab{tbname}&format=json&mode=most-recent&p1=10&p2="
    api_data = fetch_api_data(api_url)
    
    if api_data:
        # Do whatever you want with the API data here
        return api_data
    else:
        print("Failed to fetch data from the API.")


def get_since(dt,tbname=table_list[0]):

    api_url = f"http://110.49.150.135:4002/CPU/?command=DataQuery&uri=dl:tab{tbname}&format=json&mode=since-time&p1={dt}&p2="
    api_data = fetch_api_data(api_url)
    
    if api_data:
        # Do whatever you want with the API data here
        return api_data
    else:
        print("Failed to fetch data from the API.")



def get_since_long(dt_start,dt_end,tbname=table_list[0]):
    dt_start_stamp = datetime.datetime.strptime(dt_start,"%Y-%m-%d")
    dt_end_stamp = datetime.datetime.strptime(dt_end,"%Y-%m-%d")

    over_end = False
    pointer_time = dt_start_stamp

    res = []
    while not over_end:
        pointer_time_str = datetime.datetime.strftime(pointer_time,"%Y-%m-%dT%H:%M:%S")
        current_dat = get_since(pointer_time_str)['data']
        res = res + current_dat
        
        print(f'Query for time {pointer_time_str}: length = {len(current_dat)}')
        if pd.to_datetime(current_dat[-1]['time']) >= dt_end_stamp:
            over_end = True
        else:
            pointer_time = pd.to_datetime(current_dat[-1]['time'])

    cutres = [dat for dat in res if pd.to_datetime(dat['time']) <= dt_end_stamp]

    header = get_recent()['head']

    js = {'head':header,
        'data':cutres}
    
    return js


def process_json(jsonvar):
    col_list = [dat['name'] for dat in jsonvar['head']['fields']]
    ncol = len(col_list)
    for t in jsonvar['data']:
        for i in range(ncol):
            t[col_list[i]] = t['vals'][i]
        del t['vals']
    
def processed_json_to_df(jsonvar):
    df = pd.DataFrame(jsonvar['data'])

    df.drop_duplicates(subset=['time'],inplace=True)

    df['time'] = pd.to_datetime(df['time'])

    return df

def plotcol(df,col,dpi=200):
    plt.figure(dpi=dpi)
    plt.scatter(df['time'],df[col])
    plt.title(col)
    plt.xlabel('Time')
    plt.xticks(rotation=45)
    plt.ylabel(unitdict.get(col))
    plt.show()