from pymongo import MongoClient
import pandas as pd
import numpy as np
import json
import time

# Import dicts
with open('info.txt') as f:
    dictionaries = json.load(f)
roomtype_dict = dictionaries[0]
mealtype_dict = dictionaries[1]
airport_name = dictionaries[3]
global_start_date = pd.Timestamp(dictionaries[4].get("global_start_date")).date()

# Raw query
query_outbounddeparturedatetime = "2023-04-02"
query_inbounddeparturedatetime = "2023-05-20"
query_duration = 2
query_countadults = 2
query_countchildren = 1
query_price_min = 0
query_price_max = 1700
query_outbounddepartureairport = "Munich International Airport"

# Transform query
query_outbounddeparturedatetime = int((pd.Timestamp(query_outbounddeparturedatetime).date()-global_start_date).days)
query_inbounddeparturedatetime = int((pd.Timestamp(query_inbounddeparturedatetime).date()-global_start_date).days)
query_outbounddepartureairport = int([k for k, v in airport_name.items() if v == query_outbounddepartureairport][0])

# Initiate MongoClinet
client = MongoClient("mongodb://localhost:27017")
db = client['holiday-challenge']
offers = db['offers']
hotels = db['hotels']

# View 1 of search
start = time.time()
selection_1 = offers.aggregate([
    { "$match": {
        "outbounddeparturedatetime": {"$gte": query_outbounddeparturedatetime},
        "inbounddeparturedatetime": {"$lte": query_inbounddeparturedatetime},
        "price": {"$gte": query_price_min, "$lte": query_price_max},
        "countadults": query_countadults,
        "countchildren": query_countchildren,
        "outbounddepartureairport": query_outbounddepartureairport,
        "duration": query_duration
        }
    },
    { "$project": {
        "_id": 0,
        "hotelid": 1,
        "outbounddeparturedatetime": 1,
        "inbounddeparturedatetime": 1,
        "price": 1,
        "mealtype": 1,
        "roomtype": 1,
        "oceanview": 1
        }
    },
    { "$sort": { "price": 1 }},
    { "$group": {"_id": "$hotelid", "best": {"$first": "$$ROOT"}}},
    {"$sort": {"best.price": 1}},
])
for each in selection_1:
    print(each)
    offer = np.fromiter(each["best"].values(), dtype=int)
    more_info = list(hotels.aggregate([
        {"$match": {"hotelid": int(offer[3])}},
        {"$project": {"_id": 0, "hotelname": 1, "hotelstars": 1}},
    ]).next().values())
    #print(more_info)
print(time.time()-start)

# View 2 of search
query_roomtype = 10
query_mealtype = 2
query_oceanview = 0
selected_hotel = 237
start = time.time()
selection_2 = offers.aggregate([
    { "$match": {
        "outbounddeparturedatetime": {"$gte": query_outbounddeparturedatetime},
        "inbounddeparturedatetime": {"$lte": query_inbounddeparturedatetime},
        "price": {"$gte": query_price_min, "$lte": query_price_max},
        "countadults": query_countadults,
        "countchildren": query_countchildren,
        "outbounddepartureairport": query_outbounddepartureairport,
        "duration": query_duration,
        "hotelid": selected_hotel
        }
    },
    { "$project": {
        "_id": 0,
        "outbounddeparturedatetime": 1,
        "inbounddeparturedatetime": 1,
        "price": 1,
        "mealtype": 1,
        "roomtype": 1,
        "oceanview": 1
        }
    },
    { "$sort": { "price": 1 }},
])
for each in selection_2:
    offer = np.fromiter(each.values(), dtype=int)
    mask = (offer[3]==query_mealtype)*(offer[4]==query_roomtype)*(offer[5]==query_oceanview)
    if mask:
        print(offer)
print(time.time()-start)