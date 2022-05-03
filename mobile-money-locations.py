import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

all_locs = pd.DataFrame(columns=['name', 'lat', 'lon'])

# eZ Cash Communications ------------------------------------------------------
locs = pd.read_csv('data/mobile_money/ez_cash_communications.csv')

locs['name'] = 'eZ Cash Communication'
locs['lat'] = [float(loc) for loc in locs['Y']]
locs['lon'] = [float(loc) for loc in locs['X']]

locs = locs[['name', 'lat', 'lon']].drop_duplicates()
all_locs = pd.concat(objs=[all_locs, locs])

del locs

# Dialog Service Points -------------------------------------------------------
locs = BeautifulSoup(
    open('data/mobile_money/dialog_service_points.html'),
    'html.parser')
locs = [loc.get('href') for loc in locs.find_all('a')]
locs = [urlparse(loc) for loc in locs]
locs = [parse_qs(loc.query)['destination'] for loc in locs]

locs = [loc[0].split(',') for loc in locs]
locs = pd.DataFrame(data=locs, columns=['lat', 'lon'], dtype='float')
locs['name'] = 'Dialog Service Point'

locs = locs[['name', 'lat', 'lon']].drop_duplicates()
all_locs = pd.concat(objs=[all_locs, locs])

del locs

# mCash Communications --------------------------------------------------------
locs = pd.read_csv('data/mobile_money/mcash_communications.csv')
locs['store_location'] = [str(loc).replace('POINT (', '').replace(
    ')', '').split(' ') for loc in locs['store_location']]

locs['name'] = 'mCash Communication'
locs['lat'] = [float(loc[1]) for loc in locs['store_location']]
locs['lon'] = [float(loc[0]) for loc in locs['store_location']]

locs = locs[['name', 'lat', 'lon']].drop_duplicates()
all_locs = pd.concat(objs=[all_locs, locs])

del locs

# Mobitel Touch Points --------------------------------------------------------
locs = pd.read_csv('data/mobile_money/mobitel_touch_points.csv')
locs = locs[[loc in ['branch', 'touch_point', 'dealer_online']
             for loc in locs['type']]]
locs['name'] = 'Mobitel Touch Point'

locs = locs[['name', 'lat', 'lon']].drop_duplicates()
all_locs = pd.concat(objs=[all_locs, locs])

del locs

# Commercial Bank ATMs --------------------------------------------------------
locs = pd.read_json('data/mobile_money/commercial_bank_atm.json')
locs = locs.pop('children')
locs = [loc['location'] for loc_group in locs for loc in loc_group]
locs = pd.DataFrame(data=locs)

locs['name'] = 'Commercial Bank ATM'
locs['lat'] = [float(loc) for loc in locs['latitude']]
locs['lon'] = [float(loc) for loc in locs['longitude']]

locs = locs[['name', 'lat', 'lon']].drop_duplicates()
all_locs = pd.concat(objs=[all_locs, locs])

del locs

# Sampath Bank ATMs -----------------------------------------------------------
locs = pd.read_xml('data/mobile_money/sampath_bank_atm.xml')
locs = locs[locs['lat'].notna()]
locs = locs[locs['lng'].notna()]

locs['name'] = 'Sampath Bank ATM'
locs['lat'] = [float(loc) for loc in locs['lat']]
locs['lon'] = [float(loc) for loc in locs['lng']]

locs = locs[['name', 'lat', 'lon']].drop_duplicates()
all_locs = pd.concat(objs=[all_locs, locs])

del locs

# Write to disk ---------------------------------------------------------------
all_locs = all_locs.drop_duplicates(subset=['lat', 'lon'])
all_locs['id'] = range(1, len(all_locs) + 1)
all_locs = all_locs.set_index(keys='id')
all_locs.to_csv('results/mobile_money_locations.csv')
