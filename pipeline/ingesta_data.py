#!/usr/bin/env python
# coding: utf-8

# In[2]:

from sqlalchemy import create_engine
import pandas as pd
import tqdm.auto as tqdm

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

def run():
    ano = 2021
    mes = 1

    pg_user = 'root'
    pg_password = 'root'
    pg_host = 'localhost'
    pg_port = '5432'
    pg_db = 'ny_taxi'

    # Leer datos de taxi de Nueva York desde un archivo CSV comprimido en formato gzip
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    df = pd.read_csv(prefix + f'yellow_tripdata_{ano}-{mes}.csv.gz')

    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')

    target_table = 'yellow_taxi_data'
    chunksize = 100000

    df_iter = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000)

    first = True

    for df_chunk in tqdm(df_iter):

        if first:
            # Create table schema (no data)
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists="replace"
            )
            first = False
            print("Table created")

        # Insert chunk
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append"
        )

        print("Inserted:", len(df_chunk))


if __name__ == "__main__":
    run()