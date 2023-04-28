from pymongo import MongoClient
import pandas as pd

# Initiate MongoClinet
client = MongoClient("mongodb://localhost:27017")
db = client['holiday-challenge']
collection = db['hotels']

columns_needed = ["hotelid", "hotelname", "hotelstars"]
df = pd.read_csv("hotels.csv", usecols=columns_needed, sep=";")
df["hotelstars"] = df["hotelstars"].astype(int)
df["hotelid"] = df["hotelid"].astype(int)
df["hotelname"] = df["hotelname"].astype(str)
print(df)


for index, row in df.iterrows():
    insertion = {}
    for field in columns_needed:
        insertion[field] = row[field]
    collection.insert_one(insertion)
