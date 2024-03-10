'''
This script is dedicated to processing time series data for statistical analysis. 
It extends raw time series into a detailed format with individual timestamps, enabling deeper analysis.
The script calculates a variety of summary statistics to describe the central tendency, dispersion, and shape of the data.
It also performs advanced statistical tests to assess the stationarity and heteroscedasticity of the series,
which are essential properties for many time series modeling techniques.

The output is a comprehensive set of metrics for each time series, saved in a CSV file for further examination or reporting.
This automated statistical evaluation aids in the preliminary assessment of time series data, streamlining the data analysis pipeline in forecasting projects.
'''
import pandas as pd
import numpy as np
import os
import datetime
import sys
import re
from itertools import chain
from dateutil.relativedelta import relativedelta
from statsmodels.tsa.stattools import adfuller
import warnings
warnings.filterwarnings("ignore", message="divide by zero encountered in log")
import matplotlib.pyplot as plt
from arch import arch_model
try:
    from src.tables_create import convert_tsf_to_dataframe
except:
    from tables_create import convert_tsf_to_dataframe
import seaborn as sns
sns.set_style("whitegrid")

EASY_FREQUENCY_TO_RELATIVEDELTA = {
    'minutely': 'minutes',
    'hourly': 'hours',
    'daily': 'days',
    'weekly': 'weeks',
    'monthly': 'months',
    'yearly': 'years'
}


ONLY_SELECTED_DATASETS = []


def relative_time_func(frequency):
    if frequency in EASY_FREQUENCY_TO_RELATIVEDELTA:
        def relativedelta_func(value):
            return relativedelta(**{EASY_FREQUENCY_TO_RELATIVEDELTA[frequency]: value})
        return relativedelta_func
    elif frequency == 'quarterly':
        def relativedelta_func(value):
            return relativedelta(months=value*3)
        return relativedelta_func
    seconds = re.search('([0-9]+)_seconds', frequency)
    if seconds:
        seconds = int(seconds.group(1))
        def relativedelta_func(value):
            return relativedelta(seconds=value*seconds)
        return relativedelta_func
    minutes = re.search('([0-9]+)_minutes', frequency)
    if minutes:
        minutes = int(minutes.group(1))
        def relativedelta_func(value):
            return relativedelta(minutes=value*minutes)
        return relativedelta_func
    hours = re.search('([0-9]+)_hours', frequency)
    if hours:
        hours = int(hours.group(1))
        def relativedelta_func(value):
            return relativedelta(hours=value*hours)
        return relativedelta_func
    days = re.search('([0-9]+)_days', frequency)
    if days:
        days = int(days.group(1))
        def relativedelta_func(value):
            return relativedelta(days=value*days)
        return relativedelta_func
    else:
        raise Exception(f'Frequency {frequency} not supported')



def transform_dataset(dataset_raw, frequency):
    delta_frequency = relative_time_func(frequency)
    for i in range(0, len(dataset_raw.index), 100):
        partial_dataset_raw = dataset_raw.iloc[i:min(i+100, len(dataset_raw.index))]
        partial_dataset = (
            partial_dataset_raw
            .assign(timestamp=lambda df: df.apply(
                lambda row: [
                    (row.start_timestamp + delta_frequency(i)) for i in range(0, len(row.series_value))
                ], axis=1
            ))
            .drop('start_timestamp', axis=1)
            .assign(timestamp_series_value=lambda df: df.apply(
                lambda row: list(zip(row['series_value'], row['timestamp'])), axis=1
            ))
            .explode('timestamp_series_value')
            .assign(series_value=lambda df: df.apply(lambda row: row.timestamp_series_value[0], axis=1))
            .assign(timestamp=lambda df: df.apply(lambda row: row.timestamp_series_value[1], axis=1))
            .drop('timestamp_series_value', axis=1)
        )
        yield partial_dataset


def transform_entire_dataset(dataset_raw, frequency):
    delta_frequency = relative_time_func(frequency)
    dataset = dataset_raw.copy()
    dataset = (
        dataset
        .assign(timestamp=lambda df: df.apply(
            lambda row: [
                (row.start_timestamp + delta_frequency(i)) for i in range(0, len(row.series_value))
            ], axis=1
        ))
        .drop('start_timestamp', axis=1)
        .assign(timestamp_series_value=lambda df: df.apply(
            lambda row: list(zip(row['series_value'], row['timestamp'])), axis=1
        ))
        .explode('timestamp_series_value')
        .assign(series_value=lambda df: df.apply(lambda row: row.timestamp_series_value[0], axis=1))
        .assign(timestamp=lambda df: df.apply(lambda row: row.timestamp_series_value[1], axis=1))
        .drop('timestamp_series_value', axis=1)
    )
    yield dataset


def calc_summary_statistics(dataset):
    summary_statistics_dataset = (
        dataset
        .assign(series_value=lambda df: df.series_value.astype(float))
        .groupby('series_name')
        .agg({
            'timestamp': ['min', 'max', 'count'],
            'series_value': ['mean', 'std', 'median', lambda x: x.quantile(.25), lambda x: x.quantile(.75), 'skew']
        })
        .set_axis(['timestamp_min', 'timestamp_max', 'n_obs', 'mean', 'std', 'median', 'q1', 'q3', 'skew'], axis=1)
        .assign(lenght_days=lambda df: df.apply(lambda row: (row.timestamp_max - row.timestamp_min).days, axis=1))
        .assign(coef_variation=lambda df: df['std'] / df['mean'])
    )
    return summary_statistics_dataset


def test_stationarity(series):
    try:
        series_wout_na = pd.to_numeric(series, errors='coerce').dropna()
        series_wout_na = series_wout_na.map(lambda x: ((x - series_wout_na.mean()) / series_wout_na.std()))
        dist_from_one = series_wout_na.min() - 1
        series_wout_na = series_wout_na + abs(dist_from_one) if dist_from_one < 0 else series_wout_na
        adf_result = adfuller(series_wout_na)
        return {
            'adf_stat': adf_result[0],
            'adf_pvalue': adf_result[1],
        }
    except Exception as e:
        print(f'Exception in test_stationarity: {str(e)}')
        return {
            'adf_stat': np.nan,
            'adf_pvalue': np.nan,
        }


def test_heterocedasticity(series, stationary=False):
    try:
        series_wout_na = pd.to_numeric(series, errors='coerce').dropna()
        if not stationary:
            series_wout_na = series_wout_na.diff().dropna()
        series_wout_na = series_wout_na.map(lambda x: ((x - series_wout_na.mean()) / series_wout_na.std()))
        dist_from_one = series_wout_na.min() - 1
        series_wout_na = series_wout_na + abs(dist_from_one) if dist_from_one < 0 else series_wout_na
        am = arch_model(series_wout_na, vol='Arch', p=1, q=1, rescale=False)
        res = am.fit(update_freq=5, disp='off')
        heterocedasticity = (
            True if res.pvalues['alpha[1]'] < 0.05 # or res.pvalues['beta[1]'] < 0.05
            or res.pvalues['omega'] < 0.05 else False
        )
        return {
            'garch_rsquared': res.rsquared,
            'garch_alpha_pvalue': res.pvalues['alpha[1]'],
            # 'garch_beta_pvalue': res.pvalues['beta[1]'],
            'garch_omega_pvalue': res.pvalues['omega'],
            'heterocedasticity': 'Yes' if heterocedasticity else 'No'
        }
    except Exception as e:
        print(f'Exception in test_heterocedasticity: {str(e)}')
        return {
            'garch_rsquared': np.nan,
            'garch_alpha_pvalue': np.nan,
            'garch_beta_pvalue': np.nan,
            'garch_omega_pvalue': np.nan,
            'heterocedasticity': 'No'
        }
     

def calc_advanced_statistics(dataset):
    dataset_adv_stats = pd.DataFrame()
    for series_name, series in dataset.groupby('series_name'):
        series = series.series_value
        adv_stats = test_stationarity(series)
        stationary = True if adv_stats['adf_pvalue'] < 0.05 else False
        adv_stats.update(test_heterocedasticity(series, stationary))
        adv_stats.update({'series_name': series_name})
        series_adv_stats = pd.DataFrame(adv_stats, index=[0])
        dataset_adv_stats = pd.concat([dataset_adv_stats, series_adv_stats])
    return dataset_adv_stats


if __name__ == '__main__':
    tsf_databases = [tsf_file for tsf_file in os.listdir('data') if tsf_file.endswith('.tsf')]
    if ONLY_SELECTED_DATASETS:
        tsf_databases = [tsf_file for tsf_file in tsf_databases if tsf_file in ONLY_SELECTED_DATASETS]
    for tsf_file in tsf_databases:
        print(f'Processing {tsf_file}...')
        dataset_list = convert_tsf_to_dataframe(f'data/{tsf_file}')
        dataset_raw = dataset_list[0]
        dataset_name = tsf_file.replace('.tsf', '')
        dataset_frequency  = dataset_list[1]
        transformed_dataset_parts = transform_dataset(dataset_raw, dataset_frequency)
        statistics = pd.DataFrame()
        for dataset_part in transformed_dataset_parts:
            sum_statistics_part = calc_summary_statistics(dataset_part)
            adv_statistics_part = calc_advanced_statistics(dataset_part)
            statistics_part = pd.merge(sum_statistics_part, adv_statistics_part, on='series_name')
            statistics = pd.concat([statistics,  statistics_part])
        statistics.reset_index(drop=True).to_csv(f'results/summary_statistics/{dataset_name}.xlsx', index=False)