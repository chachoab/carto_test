'''
This script was used to summarize the NYC Taxi data by block.
Average daily pickups by block were calculated.
'''

# %%
import pandas as pd
import os
import geopandas
from timeit import default_timer as timer

def nyc_data_by_block(ny_path, geo_path):
    files = os.listdir(ny_path)
    columns = pd.read_csv(os.path.join(ny_path, 'yellow_tripdata_2015-01_00'), nrows=1).columns
    usecols = {
        'trip_distance',
        'pickup_longitude',
        'pickup_latitude',
        'tpep_pickup_datetime',
        'total_amount'
    }

    dtype = {
        'trip_distance': 'float32',
        'pickup_longitude': 'float32',
        'pickup_latitude': 'float32',
        'total_amount': 'float32'
    }

    geo = geopandas.read_file(geo_path)
    df_list = []
    start = timer()
    for f in files:
        if f.endswith('00'):
            ny_part = pd.read_csv(os.path.join(ny_path, f),
                usecols=usecols, dtype=dtype)
        else:
            ny_part = pd.read_csv(os.path.join(ny_path, f),
                usecols=usecols, dtype=dtype, names=columns)

        # Clean
        ny_part = ny_part[ny_part['total_amount'] >= 0]
        ny_part = ny_part[ny_part['trip_distance'] != 0]

        # Join with census groups
        ny_part = geopandas.GeoDataFrame(
            ny_part, geometry=geopandas.points_from_xy(
                ny_part['pickup_longitude'], ny_part['pickup_latitude'])
        )
        ny_part = geopandas.sjoin(ny_part, geo, how='inner', op='within')

        # Summarize
        ny_part['pickup_date'] = pd.to_datetime(ny_part['tpep_pickup_datetime'])
        ny_part['pickup_date'] = ny_part['pickup_date'].dt.floor('d')
        ny_part = ny_part.groupby(['pickup_date', 'geoid']) \
            .size().reset_index(name='avg')

        df_list.append(ny_part)

        end = timer()
        print('{}: {} seconds'.format(f, end - start))
        start = end

    #Concat and calculate average
    ny = pd.concat(df_list, ignore_index=True)
    ny = ny.groupby('geoid').mean()
    return ny

# %%
ny_path = r'..\..\data\raw\taxi data'
geo_path =r'..\..\data\raw\nyc_cbg_geoms.geojson'

# %%
%%time
ny = nyc_data_by_block(ny_path, geo_path)

# %%
ny.reset_index().to_feather('../data/interim/nyc_taxi_data_by_block.feather')
