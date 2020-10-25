# %%
import pandas as pd
import os

def clean_nyc_data(ny):
    ny = ny[ny['total_amount'] >= 0]
    ny = ny[ny['pickup_longitude'] != 0]
    ny = ny[ny['dropoff_longitude'] != 0]
    ny = ny[ny['trip_distance'] != 0]

def read_nyc_data(path, dtype, usecols=None):
    files = os.listdir(path)
    columns = pd.read_csv(os.path.join(path, 'yellow_tripdata_2015-01_00'), nrows=1).columns
    usecols = usecols if usecols else columns
    df_list = []

    for f in files:    
        if f.endswith('00'):
            df_list.append(pd.read_csv(os.path.join(path, f), usecols=usecols, dtype=dtype))
        else:
            df_list.append(pd.read_csv(os.path.join(path, f), usecols=usecols, dtype=dtype, names=columns))

    ny = pd.concat(df_list, ignore_index=True)
    return ny

# %%
dtype = {
    'VendorID': 'category',
    'passenger_count': 'int8',
    'trip_distance': 'float32',
    'pickup_longitude': 'float32',
    'pickup_latitude': 'float32',
    'dropoff_longitude': 'float32',
    'dropoff_latitude': 'float32',
    'RateCodeID': 'category',
    'store_and_fwd_flag': 'category',
    'payment_type': 'category',
    'fare_amount': 'float32',
    'extra': 'float32',
    'mta_tax': 'category',
    'tip_amount': 'float32',
    'tolls_amount': 'float32',
    'improvement_surcharge': 'category',
    'total_amount': 'float32'
}

path = r'..\data\raw\taxi data'

# %%
%%time
ny = read_nyc_data(path, dtype)

# %%
ny = clean_nyc_data(ny)

# %%
%%time
ny.to_feather('../data/raw/nyc_taxi_data.feather')

# %%
