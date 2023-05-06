# holiday-challenge

### Data preparation

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

#### Prepcrossesing in params.py
The next step is to represent categorial data of type string as integer numbers, where the mapping is done with dictionaries. To further simplify the dataset, only the date information is extracted from the deaprture times and a global start date is found as the minimum date occuring in the column *outbounddeparturedatetime*. All other dates are then replaced with the number of days to the global start date. Consequently, in our transformed dataset there are only values of type int32. This greatly reduces the storage size needed for the dataset and may improve query times when applying filters to the dataset later on.


A few of these are categorical data (e.g. mealtype). So reduce storage size and query times

In offers_database.py

---

### Django app

---

### Demonstration
