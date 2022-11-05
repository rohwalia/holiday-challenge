import streamlit as st
import datetime
from dask import dataframe as dd
import pandas as pd
import numpy as np
import airportsdata

airport_IATA = ["LEJ", "STR", "HAM", "DUS", "DRS", "FRA", "CGN", "MUC", "FMO", "SCN", "DTM", "NUE", "FKB",
                "HAJ", "KSF", "BER", "BSL", "FMM", "FDH", "BRE", "NRN", "ZRH", "PAD", "ERF", "LBC", "PRG",
                "VIE", "SZG", "EIN", "AMS", "INN", "LUX", "BLL", "LNZ", "GVA", "SXB", "KRK", "BRU", "WAW",
                "GRZ", "GRQ", "KLU", "GWT", "BRN", "BRS"] #offers["outbounddepartureairport"].unique()
airport_name = [airportsdata.load('IATA').get(key)["name"] for key in airport_IATA]
better_dtypes = {
    "hotelid": "int16",
    "departuredate": "datetime64[D]",
    "returndate": "datetime64[D]",
    "countadults": "int8",
    "countchildren": "int8",
    "price": "int32",
    "outbounddepartureairport": "string[pyarrow]",
    "mealtype": "string[pyarrow]",
    "oceanview": "bool",
    "roomtype": "string[pyarrow]",
}

st.set_page_config(layout="wide")
st.sidebar.title("Mallorca holiday")

if "hotels" not in st.session_state:
    hotels = pd.read_csv("hotels.csv", usecols=["id", "name", "category_stars"]).set_index("id")
    st.session_state["hotels"] = hotels
hotels = st.session_state.hotels

if "offers" not in st.session_state or True:
    offers = dd.read_parquet("parquet", engine="pyarrow",
                             columns=["hotelid", "departuredate", "returndate", "countadults", "countchildren",
                                      "price", "outbounddepartureairport", "mealtype", "oceanview", "roomtype"])
    offers.departuredate = offers.departuredate.str.slice(0, 10)
    offers.returndate = offers.returndate.str.slice(0, 10)
    offers = offers.astype(better_dtypes)
    st.session_state["offers"] = offers
offers = st.session_state.offers

if "view" not in st.session_state:
    st.session_state.view = False
if "chosen" not in st.session_state:
    st.session_state.chosen = 0
if "number" not in st.session_state:
    st.session_state.number = 0

def change_detail(index):
    st.session_state.view = True
    st.session_state.chosen = index
def change_forward():
    st.session_state.view = False
    st.session_state.chosen = 0

def offers_filter():
    global offers
    change_forward()
    #start = time.time()
    mask = (offers["outbounddepartureairport"] == airport_IATA[airport_name.index(st.session_state.airport)]) \
           & (offers["departuredate"] > st.session_state.departure_date) \
           & (offers["returndate"] < st.session_state.return_date) \
           & (offers["countadults"] == st.session_state.adults) \
           & (offers["countchildren"] == st.session_state.children) \
           & ((offers["returndate"]-offers["departuredate"]).dt.days == st.session_state.duration)
    offers_filtered = offers.loc[mask].compute()
    results = offers_filtered.drop(["outbounddepartureairport", "countadults", "countchildren"], axis=1).sort_values("price", ascending=True).head(1000)
    st.session_state.meals = results["mealtype"].unique()
    st.session_state.rooms = results["roomtype"].unique()
    st.session_state.number = len(results)
    results = results.groupby("hotelid", sort=False)
    st.session_state.results = results

with st.sidebar.form(key="input"):
    st.session_state.airport = st.selectbox("Departure airport", options=airport_name)
    st.session_state.duration = st.number_input("Holiday duration", min_value = 1, step=1, format = "%d")
    st.session_state.departure_date = str(st.date_input("Earliest departure date", datetime.date.today()))
    st.session_state.return_date = str(st.date_input("Latest return date", datetime.date.today()))
    st.session_state.adults = st.number_input("Number of adults", min_value = 0, step=1, format = "%d")
    st.session_state.children = st.number_input("Number of children", min_value = 0, step=1, format = "%d")
    pushed = st.form_submit_button(label="Find")
if pushed:
    offers_filter()
if "results" in st.session_state and st.session_state.number != 0:
    result_hotel = st.session_state.results.first()
    st.markdown("## Results")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.session_state.stars = st.slider('Minimum number of stars:', 0, 5, 1)
    with col2:
        st.session_state.meal = st.selectbox("Mealtype:", np.insert(st.session_state.meals, 0, "all"), index=0)
    with col3:
        st.session_state.room = st.selectbox("Roomtype:", np.insert(st.session_state.rooms, 0, "all"), index=0)
    if st.session_state.view == False:
        col1, col2, col3, = st.columns([1, 1, 1])
        col1.markdown("#### Hotel")
        col2.markdown("#### Travel details")
        st.session_state.count = 0
        for index, row in result_hotel.iterrows():
            if hotels["category_stars"].loc[index] >= st.session_state.stars:
                if st.session_state.meal == "all" or st.session_state.meal in st.session_state.results.get_group(index)["mealtype"].unique():
                    if st.session_state.room == "all" or st.session_state.room in st.session_state.results.get_group(index)["roomtype"].unique():
                        st.session_state.count = st.session_state.count + 1
                        with st.container():
                            col1, col2, col3 = st.columns([1, 1, 1])
                            with col1:
                                st.write(hotels["name"].loc[index])
                                st.write(":star:"*int(hotels["category_stars"].loc[index]))
                            with col2:
                                st.write(":heavy_dollar_sign::", row["price"])
                                st.write(":date::", row["departuredate"].strftime("%d-%B (%A)"), "to", row["returndate"].strftime("%d-%B (%A)"))
                            col3.button("More Offers", key=index, on_click=change_detail, args=(index, ))
                        st.markdown("""---""")
        if st.session_state.count == 0:
            st.write("No fitting offers found, try using less restrictive parameters!")
    if st.session_state.view == True:
        st.write("#### Offers from", hotels["name"].loc[st.session_state.chosen], ":star:"*int(hotels["category_stars"].loc[st.session_state.chosen]))
        col1, col2, col3, = st.columns([1, 1, 1])
        col1.markdown("#### Travel details")
        col2.markdown("#### Room details")
        col3.markdown("#### Price")
        st.session_state.count = 0
        for index, row in st.session_state.results.get_group(st.session_state.chosen).iterrows():
            if (row["mealtype"] == st.session_state.meal or st.session_state.meal == "all") and (row["roomtype"] == st.session_state.room or st.session_state.room == "all"):
                st.session_state.count = st.session_state.count + 1
                with st.container():
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        st.write(st.session_state.adults,"adults")
                        if st.session_state.children != 0:
                            st.write(st.session_state.children, "children")
                        st.write(":date::", row["departuredate"].strftime("%d-%B (%A)"), "to",
                                 row["returndate"].strftime("%d-%B (%A)"))
                    with col2:
                        st.write(":bed::", row["roomtype"])
                        st.write(":knife_fork_plate::", row["mealtype"])
                        if row["oceanview"]:
                            st.write(":ocean:")
                    with col3:
                        st.write(":heavy_dollar_sign::", row["price"])
                st.markdown("""---""")
        if st.session_state.count == 0:
            st.write("No fitting offers found, try using less restrictive parameters!")
        st.button("Back", key=0, on_click=change_forward)
if "results" in st.session_state and st.session_state.number == 0:
    st.write("No fitting offers found, try using less restrictive parameters!")
