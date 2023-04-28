from pymongo import MongoClient
import numpy as np
from bing_image_urls import bing_image_urls

client = MongoClient("mongodb://localhost:27017")
db = client['holiday-challenge']
hotels = db['hotels']

urls = []
for doc in hotels.find():
    name = doc["hotelname"]#.replace(" ", "+")
    if " " not in name:
        name = "Hotel "+name
    index = doc["hotelid"]-1
    print(name)

    try:
        url_list = bing_image_urls(name, limit=2)
        if "ImageHandler" in url_list[0]:
            image_url = url_list[1]
        else:
             image_url = url_list[0]
    except:
        image_url = 0

    if image_url == 0:
        urls.append("https://www.hipotels.com/content/imgsxml/hoteles/granplayadepalma-portada1765.jpg")
    else:
        urls.append(image_url)
    print(image_url)
urls = np.array(urls)
print(urls)

np.savetxt("urls.txt", urls, fmt='%s')
