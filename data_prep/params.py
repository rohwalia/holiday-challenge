import pandas as pd
import airportsdata
import dask.dataframe as dd
import json

sample_dd = dd.read_csv("offers.csv", usecols=["roomtype", "mealtype", "outbounddepartureairport", "outbounddeparturedatetime"])

# Map categorical data to integers
roomtype_dict = dict(enumerate(sample_dd['roomtype'].unique().compute()))
mealtype_dict = dict(enumerate(sample_dd['mealtype'].unique().compute()))
airport_dict = dict(enumerate(sample_dd['outbounddepartureairport'].unique().compute()))
airport_name = dict(enumerate([airportsdata.load('IATA').get(key)["name"] for key in list(airport_dict.values())]))
print(roomtype_dict)
print(mealtype_dict)
print(airport_dict)
print(airport_name)

# Define global start date
global_start_date = pd.Timestamp(sample_dd["outbounddeparturedatetime"].min().compute()).date()
print(global_start_date)

# Write mappings to txt file
info = [roomtype_dict, mealtype_dict, airport_dict, airport_name, {"global_start_date": global_start_date}]
with open('info.txt', 'w') as f:
    json.dump(info, f, default=str)