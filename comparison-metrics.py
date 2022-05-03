import numpy as np
import pandas as pd


def weighted_quantile(values, quantiles, weights):
    values = np.array(values)
    quantiles = np.array(quantiles)
    weights = np.array(weights)

    sorter = np.argsort(values)
    values = values[sorter]
    weights = weights[sorter]

    weighted_quantiles = np.cumsum(weights) - 0.5 * weights
    weighted_quantiles /= np.sum(weights)

    return np.interp(quantiles, weighted_quantiles, values)


data = pd.read_csv('data/metrics/nearest_locations.zip')

# Decile Metrics --------------------------------------------------------------
decile_bins = weighted_quantile(
    values=data['gnd_sei'],
    quantiles=np.linspace(0, 1, 11),
    weights=data['pop_count'])

data['sei_decile'] = pd.cut(
    x=data['gnd_sei'],
    bins=decile_bins,
    labels=range(1, 11),
    include_lowest=True)
del decile_bins

decile_metrics = pd.concat(objs=[
    data.groupby(by='sei_decile').apply(func=lambda x: pd.Series({
        'samurdhi_count': len(set(x['samurdhi_id'])),
        'samurdhi_dist_mean': np.average(
            a=x['samurdhi_dist'],
            weights=x['pop_count']),
        'samurdhi_dist_max': np.max(x['samurdhi_dist']),
        'supermarket_count': len(set(x['supermarket_id'])),
        'supermarket_dist_mean': np.average(
            a=x['supermarket_dist'],
            weights=x['pop_count']),
        'supermarket_dist_max': np.max(x['supermarket_dist']),
        'mobile_money_count': len(set(x['mobile_money_id'])),
        'mobile_money_dist_mean': np.average(
            a=x['mobile_money_dist'],
            weights=x['pop_count']),
        'mobile_money_dist_max': np.max(x['mobile_money_dist']),
        'potential_count': len(set(x['potential_id'])),
        'potential_dist_mean': np.average(
            a=x['potential_dist'],
            weights=x['pop_count']),
        'potential_dist_max': np.max(x['potential_dist'])})),
    data.groupby(lambda x: 'All').apply(func=lambda x: pd.Series({
        'samurdhi_count': len(set(x['samurdhi_id'])),
        'samurdhi_dist_mean': np.average(
            a=x['samurdhi_dist'],
            weights=x['pop_count']),
        'samurdhi_dist_max': np.max(x['samurdhi_dist']),
        'supermarket_count': len(set(x['supermarket_id'])),
        'supermarket_dist_mean': np.average(
            a=x['supermarket_dist'],
            weights=x['pop_count']),
        'supermarket_dist_max': np.max(x['supermarket_dist']),
        'mobile_money_count': len(set(x['mobile_money_id'])),
        'mobile_money_dist_mean': np.average(
            a=x['mobile_money_dist'],
            weights=x['pop_count']),
        'mobile_money_dist_max': np.max(x['mobile_money_dist']),
        'potential_count': len(set(x['potential_id'])),
        'potential_dist_mean': np.average(
            a=x['potential_dist'],
            weights=x['pop_count']),
        'potential_dist_max': np.max(x['potential_dist'])}))])
decile_metrics.index.name = 'sei_decile'

decile_metrics.to_csv('results/decile_metrics.csv')

# Samurdhi Metrics ------------------------------------------------------------
samurdhi_metrics = data.groupby(by='samurdhi_id') \
    .apply(func=lambda x: pd.Series({
        'pop_count': np.sum(a=x['pop_count']),
        'dist_mean': np.mean(a=x['samurdhi_dist'])}))

samurdhi_metrics.to_csv('results/samurdhi_metrics.csv')

# Supermarket Metrics ---------------------------------------------------------
supermarket_metrics = data.groupby(by='supermarket_id') \
    .apply(func=lambda x: pd.Series({
        'pop_count': np.sum(a=x['pop_count']),
        'dist_mean': np.mean(a=x['supermarket_dist'])}))

supermarket_metrics.to_csv('results/supermarket_metrics.csv')

# Mobile Money Metrics --------------------------------------------------------
mobile_money_metrics = data.groupby(by='mobile_money_id') \
    .apply(func=lambda x: pd.Series({
        'pop_count': np.sum(a=x['pop_count']),
        'dist_mean': np.mean(a=x['mobile_money_dist'])}))

mobile_money_metrics.to_csv('results/mobile_money_metrics.csv')

# Potential Metrics -----------------------------------------------------------
potential_metrics = data.groupby(by='potential_id') \
    .apply(func=lambda x: pd.Series({
        'pop_count': np.sum(a=x['pop_count']),
        'dist_mean': np.mean(a=x['potential_dist'])}))

potential_metrics.to_csv('results/potential_metrics.csv')
