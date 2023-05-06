import json
import pandas as pd
from pymongo import MongoClient
import numpy as np
import datetime

with open('holiday_app/info.txt') as f:
    dictionaries = json.load(f)
roomtype_dict = dictionaries[0]
mealtype_dict = dictionaries[1]
airport_name = dictionaries[3]
global_start_date = pd.Timestamp(dictionaries[4].get("global_start_date")).date()
with open('holiday_app/urls.txt') as file:
    urls = file.readlines()
#urls = np.loadtxt('holiday_app/urls.txt', delimiter='\n', dtype=str)

client = MongoClient("mongodb://localhost:27017")
db = client['holiday-challenge']
offers = db['offers']
hotels = db['hotels']

def get_offers(data_dict):
    query_outbounddeparturedatetime = data_dict["departure_date"]
    query_inbounddeparturedatetime = data_dict["return_date"]
    query_price_min = int(data_dict["price_min"])
    query_price_max = int(data_dict["price_max"])
    query_countadults = int(data_dict["adults"])
    query_countchildren = int(data_dict["children"])
    query_duration = int(data_dict["duration"])
    query_outbounddepartureairport = int(data_dict["airport"])
    query_outbounddeparturedatetime = int((pd.Timestamp(query_outbounddeparturedatetime).date() - global_start_date).days)
    query_inbounddeparturedatetime = int((pd.Timestamp(query_inbounddeparturedatetime).date() - global_start_date).days)
    selection_1 = offers.aggregate([
        {"$match": {
            "outbounddeparturedatetime": {"$gte": query_outbounddeparturedatetime},
            "inbounddeparturedatetime": {"$lte": query_inbounddeparturedatetime},
            "price": {"$gte": query_price_min, "$lte": query_price_max},
            "countadults": query_countadults,
            "countchildren": query_countchildren,
            "outbounddepartureairport": query_outbounddepartureairport,
            "duration": query_duration
            }
        },
        {"$project": {
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
        {"$sort": {"price": 1}},
        {"$group": {"_id": "$hotelid", "best": {"$first": "$$ROOT"}}},
        {"$sort": {"best.price": 1}},
        {"$limit": 50},
        {"$lookup": {"from": "hotels", "localField": "best.hotelid", "foreignField": "hotelid", "as": "more_info"}},
    ])
    results = []
    for each in selection_1:
        offer = np.fromiter(each["best"].values(), dtype=int)
        result_departure = (pd.Timestamp(global_start_date)+pd.Timedelta(days=offer[1])).strftime('%Y-%m-%d')
        result_return = (pd.Timestamp(global_start_date)+pd.Timedelta(days=offer[2])).strftime('%Y-%m-%d')
        result_meal = mealtype_dict[str(offer[4])].title()
        result_room = roomtype_dict[str(offer[5])].title()
        more_info_dict = each["more_info"][0]
        more_info_dict.pop('_id')
        more_info_dict.pop('hotelid')
        more_info = np.fromiter(more_info_dict.values(), dtype=object)
        """more_info = list(hotels.aggregate([
            {"$match": {"hotelid": int(offer[3])}},
            {"$project": {"_id": 0, "hotelname": 1, "hotelstars": 1}},
        ]).next().values())"""
        results.append([offer[0], result_departure, result_return, more_info[0], int(more_info[1]), result_meal, result_room, offer[6], int(offer[3]),
                        urls[int(offer[3])-1]])
    if len(results) == 0:
        results = 0
    if query_outbounddeparturedatetime>query_inbounddeparturedatetime:
        results = 1
    if query_price_max<=query_price_min:
        results = 2
    return results

def get_details(data_dict, hotel, detail_dict):
    query_outbounddeparturedatetime = data_dict["departure_date"]
    query_inbounddeparturedatetime = data_dict["return_date"]
    query_price_min = int(data_dict["price_min"])
    query_price_max = int(data_dict["price_max"])
    query_countadults = int(data_dict["adults"])
    query_countchildren = int(data_dict["children"])
    query_duration = int(data_dict["duration"])
    query_outbounddepartureairport = int(data_dict["airport"])
    query_outbounddeparturedatetime = int((pd.Timestamp(query_outbounddeparturedatetime).date() - global_start_date).days)
    query_inbounddeparturedatetime = int((pd.Timestamp(query_inbounddeparturedatetime).date() - global_start_date).days)
    selected_hotel = hotel
    query_roomtype = int(detail_dict["room_type"])-1
    query_mealtype = int(detail_dict["meal_type"])-1
    query_oceanview = int(detail_dict["ocean_view"])

    selection_2 = offers.aggregate([
        {"$match": {
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
        {"$project": {
            "_id": 0,
            "outbounddeparturedatetime": 1,
            "inbounddeparturedatetime": 1,
            "price": 1,
            "mealtype": 1,
            "roomtype": 1,
            "oceanview": 1
        }
        },
        {"$sort": {"price": 1}},
    ])
    results = []
    for each in selection_2:
        offer = np.fromiter(each.values(), dtype=int)
        mask = (offer[5] == query_oceanview)
        if query_mealtype != -1:
            mask = mask * (offer[3] == query_mealtype)
        if query_roomtype != -1:
            mask = mask * (offer[4] == query_roomtype)
        if mask:
            result_departure = (pd.Timestamp(global_start_date)+pd.Timedelta(days=offer[1])).strftime('%Y-%m-%d')
            result_return = (pd.Timestamp(global_start_date)+pd.Timedelta(days=offer[2])).strftime('%Y-%m-%d')
            result_meal = mealtype_dict[str(offer[3])].title()
            result_room = roomtype_dict[str(offer[4])].title()
            results.append([offer[0], result_departure, result_return, result_meal, result_room])
    more_info = list(hotels.aggregate([
        {"$match": {"hotelid": hotel}},
        {"$project": {"_id": 0, "hotelname": 1, "hotelstars": 1}},
    ]).next().values())
    if len(results) == 0:
        results = 0
    return results, [more_info[0], int(more_info[1]), query_oceanview, urls[hotel-1]]