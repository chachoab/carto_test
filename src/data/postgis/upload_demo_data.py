#%%
import pandas as pd
import geopandas
import numpy as np
from sqlalchemy import create_engine

# %%
%%time
demo = pd.read_csv(r'..\..\data\raw\nyc_demo_demographics.csv')

# Pivot table
demo = demo.pivot(index='geoid', columns='demo_demog_var', values='value')

# Join with geojson
block = geopandas.read_file(r'..\..\data\raw\nyc_cbg_geoms.geojson')
block['geoid'] = block['geoid'].astype(np.int64)
demo = demo.drop(columns='aggregate_travel_time_to_work')
demo = block.merge(demo, on='geoid', how='inner')
demo = demo.set_index('geoid')

# Set missing values to mean of adjacent blocks
for index, block in demo.iterrows():
    null_cols = block[block.isnull()].index.to_list()
    if null_cols:
        neighbors = demo[~demo['geometry'].disjoint(block['geometry'])].index.to_list()
        for col in null_cols:
            demo.at[index, col] = demo.loc[neighbors, col].mean()


# %%
%%time
user = input('User:')
password = input('Password')

engine = create_engine('postgresql://{}:{}@localhost:5432/carto'.format(user, password))
demo.reset_index() \
    .to_postgis('demo', engine, if_exists='append', index=False)
engine.execute('ALTER TABLE demo DROP COLUMN geometry')
# %%
