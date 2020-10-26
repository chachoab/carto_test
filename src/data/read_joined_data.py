# Get data
#%%
from sqlalchemy import create_engine
import geopandas

# %%
%%time
user = input('User:')
password = input('Password')

engine = create_engine('postgresql://{}:{}@localhost:5432/carto'.format(user, password))
sql = """
    SELECT geoid, AVG(pickups) AS avg_pickups FROM 
        (SELECT geoid, COUNT(*) AS pickups FROM trip INNER JOIN block 
        ON ST_Within(trip.geometry, block.geometry) 
        GROUP BY geoid, date_trunc('day', trip.tpep_pickup_datetime)) AS A
    GROUP BY geoid
        """
df = geopandas.read_postgis()
# %%
