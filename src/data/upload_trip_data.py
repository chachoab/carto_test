# Data was previously imported using psql command \copy
#%%
from sqlalchemy import create_engine

# %%
%%time
user = input('User:')
password = input('Password')

engine = create_engine('postgresql://{}:{}@localhost:5432/carto'.format(user, password))
engine.execute('ALTER TABLE trip ADD COLUMN pickup_geom geometry(Geometry, 4326);')
engine('UPDATE trip SET pickup_geom = ST_MakePoint(pickup_longitude, pickup_latitude);') #--> 10min!
# %%
