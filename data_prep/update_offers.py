from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://localhost:27017")
db = client['holiday-challenge']
offers = db['offers']
x = offers.update_many({}, [{"$set": {"duration": {"$subtract": ["$inbounddeparturedatetime", "$outbounddeparturedatetime"]}}}])
print(x.modified_count, "documents updated.")