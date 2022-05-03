import pandas as pd
import numpy as np

from requests import request
from bs4 import BeautifulSoup

# Get all Districts -----------------------------------------------------------
resp = request(
    method='GET',
    url='https://www.samurdhi.gov.lk/web/index.php/en/contact-us/test.html')
resp = BeautifulSoup(resp.content, 'html.parser')

dists = resp.find(id='dis').find_all('option')
dists = [dist['value'] for dist in dists]
dists = dists[1:]

del resp

# Get DSDs --------------------------------------------------------------------
dsds = {}
for dist in dists:
    resp = request(
        method='POST',
        url='https://www.samurdhi.gov.lk/web/index.php/en/contact-us/test.html',
        data={'dis': dist})
    resp = BeautifulSoup(resp.content, 'html.parser')

    new_dsds = resp.find(id='div').find_all('option')
    new_dsds = [dsd['value'] for dsd in new_dsds]
    new_dsds = new_dsds[1:]

    dsds[dist] = new_dsds
    del dist, resp, new_dsds

# Get all Samurdhi Bank locations ---------------------------------------------
locs = pd.DataFrame(columns=['dist_name', 'dsd_name', 'bank_name'])
for dist in dists:
    for dsd in dsds[dist]:
        resp = request(
            method='POST',
            url='https://www.samurdhi.gov.lk/web/index.php/en/contact-us/test.html',
            data={'dis': dist, 'div': dsd})
        resp = BeautifulSoup(resp.content, 'html.parser')

        dist_name = resp.find(id='dis').find(selected='selected').get_text()
        dsd_name = resp.find(id='div').find(selected='selected').get_text()

        new_locs = resp.find(id='tblsamurdhisheet').find_all('tr')
        new_locs = [loc.find_all('td') for loc in new_locs[4:]]
        new_locs = [loc[1].get_text() for loc in new_locs]

        new_locs = pd.DataFrame({
            'dist_name': dist_name,
            'dsd_name': dsd_name,
            'bank_name': new_locs})
        locs = pd.concat(objs=[locs, new_locs])
        del dsd, resp, dist_name, dsd_name, new_locs
    del dist
del dists, dsds

locs = locs[['Headquarters' not in name for name in locs['bank_name']]]
locs = locs[['Maha Sangam' not in name for name in locs['bank_name']]]
locs.to_csv('data/samurdhi/samurdhi_bank_list.csv', index=False)

# Simulate locations based on population distribution -------------------------
locs = pd.merge(
    left=pd.read_csv('data/samurdhi/samurdhi_bank_list.csv'),
    right=pd.read_csv('data/samurdhi/dsd_codes.csv'),
    on=['dist_name', 'dsd_name'])

pop_dist = pd.read_csv('data/samurdhi/dsd_population_distribution.zip')

sim_locs = pd.DataFrame()
rng = np.random.default_rng(2022)
for dsd_code in set(locs['code_4']):
    pot_locs = pop_dist[pop_dist['code_4'] == dsd_code]
    num_locs = locs[locs['code_4'] == dsd_code].shape[0]
    prob_locs = pot_locs['pop_count'] / np.sum(pot_locs['pop_count'])

    new_locs = rng.choice(
        a=pot_locs,
        size=num_locs,
        replace=False,
        p=prob_locs)
    new_locs = pd.DataFrame(data=new_locs, columns=pop_dist.columns)

    sim_locs = pd.concat(objs=[sim_locs, new_locs])
    del dsd_code, pot_locs, num_locs, prob_locs, new_locs
sim_locs = sim_locs[['lat', 'lon']]

# Write to disk ---------------------------------------------------------------
sim_locs['id'] = range(1, len(sim_locs) + 1)
sim_locs = sim_locs.set_index(keys='id')
sim_locs.to_csv('results/samurdhi_locations.csv')
