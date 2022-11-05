from dask import dataframe as dd

better_dtypes = {
    "hotelid": "int16",
    "departuredate": "object",
    "returndate": "object",
    "countadults": "int8",
    "countchildren": "int8",
    "price": "int16",
    "inbounddepartureairport": "string[pyarrow]",
    "inboundarrivalairport": "string[pyarrow]",
    "inboundairline": "string[pyarrow]",
    "inboundarrivaldatetime": "object",
    "outbounddepartureairport": "string[pyarrow]",
    "outboundarrivalairport": "string[pyarrow]",
    "outboundairline": "string[pyarrow]",
    "outboundarrivaldatetime": "object",
    "mealtype": "string[pyarrow]",
    "oceanview": "bool",
    "roomtype": "string[pyarrow]",
}
offers = dd.read_csv('offers.csv')
print("CSV file read")
offers.repartition(partition_size="100MB").to_csv("csvs")
print("CSV file repartitioned")
offers = dd.read_csv("csvs/*.part")
offers.to_parquet("parquet", engine="pyarrow", compression="snappy")
print("Data saved as parquet files")