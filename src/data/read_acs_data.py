'''
This script reads the ACS dataset and joins it with the goejson block data.
Then it completes null values with the mean of the adjacent blocks where possible.
Finally the data is stored in feather format.
'''
#%%
import pandas as pd
import geopandas
import numpy as np

acs = pd.read_csv(r'..\..\data\raw\nyc_acs_demographics.csv')

# Pivot table
acs = acs.pivot(index='geoid', columns='acs_demog_var', values='value')

# Join with geojson
geo = geopandas.read_file(r'..\..\data\raw\nyc_cbg_geoms.geojson')
geo['geoid'] = geo['geoid'].astype(np.int64)
acs = acs.drop(columns='aggregate_travel_time_to_work')
acs = geo.merge(acs, on='geoid', how='inner')
acs = acs.set_index('geoid')

# Set missing values to mean of adjacent blocks
for index, block in acs.iterrows():
    null_cols = block[block.isnull()].index.to_list()
    if null_cols:
        neighbors = acs[~acs['geometry'].disjoint(block['geometry'])].index.to_list()
        for col in null_cols:
            acs.at[index, col] = acs.loc[neighbors, col].mean()

acs.to_feather(r'..\..\data\interim\acs.feather')