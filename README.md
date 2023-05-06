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

For data preprocessing all relevant files can be found in the directory *data_prep*.

#### Transforming offers dataset with params.py
The next step is to represent categorial data of type string as integer numbers, where the mapping is done with dictionaries. To further simplify the dataset, only the date information is extracted from the deaprture times and a global start date is found as the minimum date occuring in the column *outbounddeparturedatetime*. All other dates are then replaced with the number of days to the global start date. Consequently, in our transformed dataset there are only values of type int32. This greatly reduces the storage size needed for the dataset and may improve query times when applying filters to the dataset later on. The dictionaries and the global start date are stored in the file *info.txt* to convert the values back to the original dates and strings.

#### Writing offers dataset to database with offers_database.py / update.offers.py
The transformed offers dataset is then stored in a MongoDB database. This is done by continously reading rows from the *offers.csv*, transforming the values and writing them to the offers collection as documents. It took about a day for all ~103m rows. Since one filter for the user should be the the duration of the holiday another column *duration* is added to the collection by calculating the difference in days between *inbounddeparturedatetime* and *outbounddeparturedatetime*. Doing this beforehand and not when the query is run, will decrease query times.

#### Writing hotels dataset to database with hotels_database.py
Since there are only ~1k different hotels, there is no need to tranform this dataset and hence it can be directly written to the hotels collection.

#### Finding images for hotels with images.py
To make the application more realistic and immersive, for each hotel a corresponding image is found. For this the library bing_image_urls is used, which gives us the url of the first image when a hotelname is looked up on the bing search engine. If there are no results or if something other than an image url is returned, a predefined default image url is used instead. The resulting list of image urls (in the order of hotelid) is written to the file *urls.txt*.

#### Testing some queries with sample_query.py
There are two types of queries needed for the application. Both use the MongoDB aggregate operation, which allows us to specify a pipeline to filter, group and sort the dataset. To decrease the query times, a covered index was created for both the offers and the hotels collection. This means, when running a query, only the index in cache is used and no document is pulled from the collection in the database. For query type 1, the actual query takes about (~75ms). However, if one adds the time taken to join the column *hotelid* from the hotels collection with the one in the query output, the total time is ~250ms. **Potential to improve: Add the columns *hotelname* and *hotelstars* to the offers collection, reducing the total time to ~100ms.** For query type 2, the query time is ~50ms.

---

### Django application

For the user to interact with MongDB database, a Django application was created and can be found in the directory *holiday_search*. In *holiday_search\holiday_search* the relevant files are *settings.py* and *urls.py*. The former is used to specify general settings, such as the location of the HTML templates. The latter maps the url extensions to the function to be called to render the application. In *holiday_search\holiday_app*. The relevant files are *form_basic.py*, *query.py* and *views.py*.


---

### Demonstration
