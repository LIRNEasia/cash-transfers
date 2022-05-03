import numpy as np
import pandas as pd
import math
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans

# Functions for clustering nearby locations -----------------------------------


def distance(orig, dest):
    lat1, lon1 = orig[0], orig[1]
    lat2, lon2 = dest[0], dest[1]
    radius = 6371  # km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat/2) * math.sin(d_lat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(d_lon/2) * math.sin(d_lon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d


def create_clusters(num_clusts, locs):
    kmeans = KMeans(n_clusters=num_clusts, random_state=2022).fit(locs)
    l_array = np.array([[label] for label in kmeans.labels_])
    clusts = np.append(locs, l_array, axis=1)
    return clusts


def validate_solution(max_dist, clusts):
    _, __, num_clusts = clusts.max(axis=0)
    num_clusts = int(num_clusts)
    for i in range(num_clusts):
        clust_2d = clusts[clusts[:, 2] == i][:, np.array([True, True, False])]
        if not validate_cluster(max_dist=max_dist, clust=clust_2d):
            return False
        else:
            continue
    return True


def validate_cluster(max_dist, clust):
    distances = cdist(
        XA=clust,
        XB=clust,
        metric=lambda orig, dest: distance(orig=orig, dest=dest))
    for item in distances.flatten():
        if item > max_dist:
            return False
    return True


def cluster_nearby_locations(max_dist, locs):
    for i in range(2, len(locs)):
        print(str(i) + '/' + str(len(locs)))
        clusts = create_clusters(num_clusts=i, locs=locs)
        if validate_solution(max_dist=max_dist, clusts=clusts):
            break
    clusts = pd.DataFrame(data=clusts, columns=['lat', 'lon', 'clust'])
    clusts = clusts.groupby(by='clust').agg({'lat': 'mean', 'lon': 'mean'})
    clusts = clusts.reset_index().drop(columns='clust')
    return clusts


all_locs = pd.DataFrame(columns=['name', 'lat', 'lon'])

# Bank of Ceylon --------------------------------------------------------------
locs = pd.read_json('data/bank/bank_of_ceylon.json')

locs = np.array(object=locs[['lat', 'lng']], dtype='float')
locs = np.unique(ar=locs, axis=0)
locs = cluster_nearby_locations(max_dist=0.1, locs=locs)

locs['name'] = 'Bank of Ceylon'
locs = locs.astype({'name': 'string', 'lat': 'float', 'lon': 'float'})
all_locs = pd.concat(objs=[all_locs, locs])

del locs

# Cargills Bank ---------------------------------------------------------------
locs = pd.read_json('data/bank/cargills_bank.json')

locs = np.array(object=locs[['lat', 'lng']], dtype='float')
locs = np.unique(ar=locs, axis=0)
locs = cluster_nearby_locations(max_dist=0.1, locs=locs)

locs['name'] = 'Cargills Bank'
locs = locs.astype({'name': 'string', 'lat': 'float', 'lon': 'float'})
all_locs = pd.concat(objs=[all_locs, locs])

del locs

# Commercial Bank of Ceylon ---------------------------------------------------
locs = pd.concat(objs=[
    pd.read_json('data/bank/commercial_bank_atm.json'),
    pd.read_json('data/bank/commercial_bank_branch.json')])
locs = locs.pop('children')
locs = [loc['location'] for loc_group in locs for loc in loc_group]
locs = pd.DataFrame(data=locs)

locs = np.array(object=locs[['latitude', 'longitude']], dtype='float')
locs = np.unique(ar=locs, axis=0)
locs = cluster_nearby_locations(max_dist=0.1, locs=locs)

locs['name'] = 'Commercial Bank of Ceylon'
locs = locs.astype({'name': 'string', 'lat': 'float', 'lon': 'float'})
all_locs = pd.concat(objs=[all_locs, locs])

del locs

# DFCC Bank -------------------------------------------------------------------
locs = pd.read_json('data/bank/dfcc_bank.json')

locs = np.array(object=locs[['lat', 'lng']], dtype='float')
locs = np.unique(ar=locs, axis=0)
locs = cluster_nearby_locations(max_dist=0.1, locs=locs)

locs['name'] = 'DFCC Bank'
locs = locs.astype({'name': 'string', 'lat': 'float', 'lon': 'float'})
all_locs = pd.concat(objs=[all_locs, locs])

del locs

# Hatton National Bank --------------------------------------------------------
locs = pd.read_json('data/bank/hatton_national_bank.json')
locs = locs[locs['latitude'].astype(bool)]
locs = locs[locs['longitude'].astype(bool)]

locs = np.array(object=locs[['latitude', 'longitude']], dtype='float')
locs = np.unique(ar=locs, axis=0)
locs = cluster_nearby_locations(max_dist=0.1, locs=locs)

locs['name'] = 'Hatton National Bank'
locs = locs.astype({'name': 'string', 'lat': 'float', 'lon': 'float'})
all_locs = pd.concat(objs=[all_locs, locs])

del locs

# National Development Bank ---------------------------------------------------
locs = pd.read_json('data/bank/national_development_bank.json')
locs = locs[locs['geo_code'].astype(bool)]
locs['lat'] = [loc.split(',')[0] for loc in locs['geo_code']]
locs['lon'] = [loc.split(',')[1] for loc in locs['geo_code']]

locs = np.array(object=locs[['lat', 'lon']], dtype='float')
locs = np.unique(ar=locs, axis=0)
locs = cluster_nearby_locations(max_dist=0.1, locs=locs)

locs['name'] = 'National Development Bank'
locs = locs.astype({'name': 'string', 'lat': 'float', 'lon': 'float'})
all_locs = pd.concat(objs=[all_locs, locs])

del locs

# Nations Trust Bank ----------------------------------------------------------
locs = pd.concat(objs=[
    pd.read_json('data/bank/nations_trust_bank_atm.json'),
    pd.read_json('data/bank/nations_trust_bank_branch.json')])

locs = np.array(object=locs[[1, 2]], dtype='float')
locs = np.unique(ar=locs, axis=0)
locs = cluster_nearby_locations(max_dist=0.1, locs=locs)

locs['name'] = 'Nations Trust Bank'
locs = locs.astype({'name': 'string', 'lat': 'float', 'lon': 'float'})
all_locs = pd.concat(objs=[all_locs, locs])

del locs

# People's Bank ---------------------------------------------------------------
locs_atm = pd.read_json('data/bank/peoples_bank_atm.json')
locs_atm['lat'] = locs_atm['lat']
locs_atm['lon'] = locs_atm['lng']

locs_branch = pd.read_json('data/bank/peoples_bank_branch.json')
locs_branch['lat'] = [loc['lat'] for loc in locs_branch['position']]
locs_branch['lon'] = [loc['lng'] for loc in locs_branch['position']]

locs = pd.concat(objs=[locs_atm, locs_branch])
del locs_atm, locs_branch

locs = np.array(object=locs[['lat', 'lon']], dtype='float')
locs = np.unique(ar=locs, axis=0)
locs = cluster_nearby_locations(max_dist=0.1, locs=locs)

locs['name'] = 'People\'s Bank'
locs = locs.astype({'name': 'string', 'lat': 'float', 'lon': 'float'})
all_locs = pd.concat(objs=[all_locs, locs])

del locs

# Sampath Bank ----------------------------------------------------------------
locs = pd.read_xml('data/bank/sampath_bank.xml')
locs = locs[locs['lat'].notna()]
locs = locs[locs['lng'].notna()]

locs = np.array(object=locs[['lat', 'lng']], dtype='float')
locs = np.unique(ar=locs, axis=0)
locs = cluster_nearby_locations(max_dist=0.1, locs=locs)

locs['name'] = 'Sampath Bank'
locs = locs.astype({'name': 'string', 'lat': 'float', 'lon': 'float'})
all_locs = pd.concat(objs=[all_locs, locs])

del locs

# Seylan Bank -----------------------------------------------------------------
locs = pd.read_json('data/bank/seylan_bank.geojson')
locs['lat'] = [loc['geometry']['coordinates'][1] for loc in locs['features']]
locs['lon'] = [loc['geometry']['coordinates'][0] for loc in locs['features']]

locs = np.array(object=locs[['lat', 'lon']], dtype='float')
locs = np.unique(ar=locs, axis=0)
locs = cluster_nearby_locations(max_dist=0.1, locs=locs)

locs['name'] = 'Seylan Bank'
locs = locs.astype({'name': 'string', 'lat': 'float', 'lon': 'float'})
all_locs = pd.concat(objs=[all_locs, locs])

del locs

# Existing Locations ----------------------------------------------------------
locs = pd.read_csv('results/mobile_money_locations.csv')
locs = locs[~locs['name'].isin(['Commercial Bank ATM', 'Sampath Bank ATM'])]
locs = locs.drop(columns='id')
all_locs = pd.concat(objs=[locs, all_locs])

del locs

# Write to disk ---------------------------------------------------------------
all_locs['id'] = range(1, len(all_locs) + 1)
all_locs = all_locs.set_index(keys='id')
all_locs.to_csv('results/potential_locations.csv')
