import numpy as np
import pandas as pd

import googlemaps
import itertools
import time

from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder

# Google Maps approach --------------------------------------------------------
gmaps = googlemaps.Client(key='') # Add API key here

locs = []
search_grid = list(itertools.product(
    np.linspace(start=5.96836985923, stop=9.82407766361, num=20),
    np.linspace(start=79.6951668639, stop=81.7879590189, num=10)))

for search_loc in search_grid:
    gmaps_result = gmaps.places(
        query="keells",
        location=search_loc,
        # radius=3500,
        region='lk')

    for loc in gmaps_result['results']:
        if loc['place_id'] not in [loc['place_id'] for loc in locs]:
            locs.append(loc)

    while 'next_page_token' in gmaps_result:
        time.sleep(2)
        gmaps_result = gmaps.places(page_token=gmaps_result['next_page_token'])
        for loc in gmaps_result['results']:
            if loc['place_id'] not in [loc['place_id'] for loc in locs]:
                locs.append(loc)

locs = [loc['name'] for loc in locs]

# OpenStreetMap approach ------------------------------------------------------
osm_query = overpassQueryBuilder(
    area=Nominatim().query('LK').areaId(),
    elementType=['node', 'way'],
    selector=['"name"~"Keells|Keels|Kells"'],
    includeCenter=True)
osm_result = Overpass().query(osm_query, timeout=1000)

locs = pd.DataFrame(osm_result.toJSON()['elements'])

# Manual approach -------------------------------------------------------------
locs = pd.read_csv('data/supermarket/supermarket_locations.csv')

locs['store_location'] = [str(loc).replace('POINT (', '').replace(
    ')', '').split(' ') for loc in locs['store_location']]
locs['name'] = [name.capitalize() for name in locs['chain']]
locs['lat'] = [float(loc[1]) for loc in locs['store_location']]
locs['lon'] = [float(loc[0]) for loc in locs['store_location']]

locs = locs[['name', 'lat', 'lon']].drop_duplicates()

# Write to disk ---------------------------------------------------------------
locs['id'] = range(1, len(locs) + 1)
locs = locs.set_index(keys='id')
locs.to_csv('results/supermarket_locations.csv')
