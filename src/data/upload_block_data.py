#%%
import pandas as pd
import geopandas
from sqlalchemy import create_engine

#%%
%%time
block = geopandas.read_file(r'..\..\data\raw\nyc_cbg_geoms.geojson')
user = input('User:')
password = input('Password')

engine = create_engine('postgresql://{}:{}@localhost:5432/carto'.format(user, password))
block.reset_index() \
    .to_postgis('block', engine, index=False)
