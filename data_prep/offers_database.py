from pymongo import MongoClient
import pandas as pd
import json

with open('info.txt') as f:
    dictionaries = json.load(f)
roomtype_dict = dictionaries[0]
mealtype_dict = dictionaries[1]
airport_dict = dictionaries[2]
global_start_date = pd.Timestamp(dictionaries[4].get("global_start_date")).date()

# Initiate MongoClinet
client = MongoClient("mongodb://localhost:27017")
db = client['holiday-challenge']
collection = db['offers']

columns_needed = ["hotelid", "outbounddeparturedatetime", "inbounddeparturedatetime", "countadults", "countchildren",
                   "price", "outbounddepartureairport", "mealtype", "roomtype", "oceanview"]
count = 0
for chunk in pd.read_csv("offers.csv", usecols=columns_needed, chunksize=10 ** 5):
    chunk.dropna(inplace=True)
    chunk["roomtype"] = chunk["roomtype"].map((dict(map(reversed, roomtype_dict.items()))))
    chunk["mealtype"] = chunk["mealtype"].map((dict(map(reversed, mealtype_dict.items()))))
    chunk["outbounddepartureairport"] = chunk["outbounddepartureairport"].map((dict(map(reversed, airport_dict.items()))))
    chunk["oceanview"] = chunk["oceanview"].astype(int)
    chunk["outbounddeparturedatetime"] = (pd.to_datetime(chunk["outbounddeparturedatetime"], utc=True).dt.date-global_start_date).dt.days
    chunk["inbounddeparturedatetime"] = (pd.to_datetime(chunk["inbounddeparturedatetime"], utc=True).dt.date - global_start_date).dt.days
    chunk = chunk.astype(int)

    for index, row in chunk.iterrows():
        insertion = {}
        for field in columns_needed:
            insertion[field] = row[field]
        for k, v in insertion.items():
            insertion[k] = int(v)
        collection.insert_one(insertion)
    print(count)
    count = count + 1