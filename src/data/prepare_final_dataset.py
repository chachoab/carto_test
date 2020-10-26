'''
This script reads and combines the folowing datasets:
    
 - acs.feather: generated from the read_acs_data.py script,
 includes processed demographic data and block geometry.
 
 - nyc_taxi_data_by_block.feather: generated with the read_nyc_data_by_block.py
 script, includes average daily pickups by geoid.

The resulting file will be used for the model 
'''
# %%
import pandas as pd
import numpy as np
import geopandas

# Join datasets
acs = geopandas.read_feather(r'..\..\data\interim\acs.feather')
ny = pd.read_feather(r'..\..\data\interim\nyc_taxi_data_by_block.feather')
ny['geoid'] = ny['geoid'].astype(np.int64)
ny = ny.set_index('geoid')
df = acs.merge(ny, how='left', on='geoid')

# Remove empty average pickups, fill remaining NA's with mean and save
df = df[df['avg'].notnull()]
df.fillna(df.mean())

df.to_csv(r'..\..\data\final\final.csv')