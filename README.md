# holiday-challenge

## Data preparation

After a first look at the offers dataset, the columns necessary for our application are:
- hotelid
- outbounddeparturedatetime
- inbounddeparturedatetime
- countadults
- countchildren
- price
- outbounddepartureairport
- mealtype
- roomtype
- oceanview

From the hotels dataset, the following are needed:
- hotelid
- hotelname
- hotelstars

#### Transforming offers dataset with params.py
The next step is to represent categorial data of type string as integer numbers, where the mapping is done with dictionaries. To further simplify the dataset, only the date information is extracted from the deaprture times and a global start date is found as the minimum date occuring in the column *outbounddeparturedatetime*. All other dates are then replaced with the number of days to the global start date. Consequently, in our transformed dataset there are only values of type int32. This greatly reduces the storage size needed for the dataset and may improve query times when applying filters to the dataset later on. The dictionaries and the global start date are stored in the file *info.txt* to convert the values back to the original dates and strings.

#### Writing offers dataset to database with offers_database.py / update.offers.py
The transformed offers dataset is then stored in a Mongo database. This is done by continously reading rows from the *offers.csv*, transforming the values and writing them to the offers collection as documents. It took about a day for all ~103m rows. Since one filter for the user should be the the duration of the holiday another column *duration* is added to the collection by calculating the difference in days between *inbounddeparturedatetime* and *outbounddeparturedatetime*. Doing this beforehand and not when the query is run, will decrease query times.

#### Writing hotels dataset to database with hotels_database.py
Since there are only ~1k different hotels, there is no need to tranform this dataset and hence it can be directly written to the hotels collection.

#### Finding images for hotels with images.py
To make the application more realistic and immersive, for each hotel a corresponding image is found. For this the library bing_image_urls is used, which gives us the url of the first image when a hotelname is looked up on the bing search engine. If there are no results or if something other than an image url is returned, a predefined default image url is used instead. The resulting list of image urls (in the order of hotelid) is written to the file *urls.txt*.

---

### Django app


---

### Demonstration
