'''
This script contains a suite of tests for verifying the integrity and correctness of 'table2.csv', a table generated in a previous step of the workflow. The tests ensure that:

- 'table2.csv' exists within the specified output directory.
- There are no missing values in the 'Dataset' column of the table, each dataset name is a string, and there are no duplicates.
- All numerical entries in the table are non-negative.
- Selected key results in the table match expected values within a tolerance level, ensuring the replication's accuracy.

The script uses the pytest framework for testing, which allows for automated, descriptive, and modular testing. The 'test_logic_table2' function checks basic DataFrame integrity,
'test_content_table2' validates specific content against known results, and 'test_generate_table2' confirms the existence of the file.

When run directly, this script will execute all tests to provide immediate feedback on the data quality and consistency of 'table2.csv', aiding in maintaining the reliability of the data analysis process.

We generally this script with "pytest".
'''
import pandas as pd
import pytest
import os
import numpy as np


import config
from pathlib import Path

DATA_DIR = config.DATA_DIR
BASE_DIR = config.BASE_DIR



table2_paper_results = pd.DataFrame({
    'Dataset': [
        'M1 Yearly', 'M1 Quarterly', 'M1 Monthly', 'M3 Yearly',
        'M3 Quarterly', 'M3 Monthly', 'M3 Other', 'M4 Yearly',
        'M4 Quarterly', 'M4 Monthly', 'M4 Weekly', 'M4 Daily',
        'M4 Hourly', 'Tourism Yearly', 'Tourism Quarterly',
        'Tourism Monthly', 'CIF 2016', 'Aus. Elecdemand',
        'Dominick', 'Bitcoin', 'Pedestrians', 'Vehicle Trips',
        'KDD', 'Weather', 'NN5 Daily', 'NN5 Weekly', 'Kaggle Daily',
        'Kaggle Weekly', 'Solar 10 Mins', 'Solar Weekly',
        'Electricity Hourly', 'Electricity Weekly', 'Carparts', 'FRED-MD',
        'Traffic Hourly', 'Traffic Weekly', 'Rideshare', 'Hospital',
        'COVID', 'Temp. Rain', 'Sunspot', 'Saugeen',
        'Births'
    ],
    'SES': [
        4.938, 1.929, 1.379, 3.167, 1.417, 1.091, 3.089, 3.981, 1.417,
        1.15, 0.587, 1.154, 11.607, 3.253, 3.21, 3.306, 1.291, 1.857,
        0.582, 4.327, 0.957, 1.224, 1.645, 0.677, 1.521, 0.903, 0.924,
        0.698, 1.451, 1.215, 4.544, 1.536, 0.897, 0.617, 1.922, 1.116,
        3.014, 0.813, 7.776, 1.347, 0.128, 1.426, 4.343
    ],
    'Theta': [
        4.191, 1.702, 1.091, 2.774, 1.117, 0.864, 2.271, 3.375, 1.231,
        0.97, 0.546, 1.153, 11.524, 3.015, 1.661, 1.649, 0.997, 1.867,
        0.61, 4.344, 0.958, 1.244, 1.646, 0.749, 0.885, 0.885, 0.928, 
        0.694, 1.452, 1.224, 4.545, 1.476, 0.914, 0.698, 1.922, 1.121, 
        3.641, 0.761, 7.793, 1.368, 0.128, 1.425, 2.138
    ],
    'TBATS': [
        3.499, 1.694, 1.118, 3.127, 1.256, 0.861, 1.848, 3.437, 1.186,
        1.053, 0.504, 1.157, 2.663, 3.685, 1.835, 1.751, 0.861, 1.174,
        0.722, 4.611, 1.297, 1.86, 1.394, 0.689, 0.858, 0.872, 0.947,
        0.622, 3.936, 0.916, 3.69, 0.792, 0.998, 0.502, 2.482, 1.148,
        3.067, 0.768, 5.719, 1.227, 0.067, 1.477, 1.453
    ],
    'ETS': [
        3.771, 1.658, 1.074, 2.86, 1.17, 0.865, 1.814, 3.444, 1.161,
        0.948, 0.575, 1.239, 26.69, 3.395, 1.592, 1.526, 0.841, 5.663,
        0.595, 2.718, 1.19, 1.305, 1.787, 0.702, 0.865, 0.911, 1.231,
        0.77, 1.451, 1.134, 6.501, 1.526, 0.925, 0.468, 2.294, 1.125,
        4.04, 0.765, 5.326, 1.401, 0.128, 2.036, 1.529
    ],
    '(DHR-) ARIMA': [
        4.479, 1.787, 1.164, 3.417, 1.24, 0.873, 1.831, 3.876, 1.228,
        0.962, 0.55, 1.179, 13.557, 3.775, 1.782, 1.589, 0.929, 2.574,
        0.796, 4.03, 3.947, 1.282, 1.982, 0.746, 1.013, 0.887, 0.89, 0.815,
        1.034, 0.848, 4.602, 0.878, 0.926, 0.533, 2.535, 1.191, 1.53,
        0.787, 6.117, 1.174, 0.067, 1.485, 1.917
    ],
    'PR': [
        4.588, 1.892, 1.123, 3.223, 1.248, 1.010, 2.655,
        3.625, 1.316, 1.080, 0.481, 1.162, 1.662, 3.516,
        1.643, 1.678, 1.019, 0.780, 0.980, 2.664, 0.256,
        1.212, 1.265, 3.046, 1.263, 0.854, np.nan, 1.021,
        1.451, 1.053, 2.912, 0.916, 0.755, 8.827, 1.281,
        1.122, 3.019, 0.782, 8.731, 0.876, 0.099, 1.674,
        2.094
    ],
    'Cat Boost': [
        4.427, 2.031, 1.209, 3.788, 1.441, 1.065, 3.178,
        3.649, 1.338, 1.093, 0.615, 1.593, 1.771, 3.553,
        1.793, 1.699, 1.175, 0.705, 1.038, 2.888, 0.262,
        1.176, 1.233, 0.762, 0.973, 0.853, np.nan, 1.928, 2.504,
        1.530, 2.262, 0.815, 0.853, 0.947, 1.571, 1.116,
        2.908, 0.798, 8.241, 1.028, 0.059, 1.411, 1.609
    ],
})


def test_generate_table2():
    '''test if table2 exists in the output directory. It already gives an idea if the problem in other tests is due to that'''
    file_path = os.path.join(BASE_DIR, 'output', 'tables', 'table2.csv')
    assert os.path.exists(file_path)


def test_logic_table2():
    '''Test if the numbers make sense'''
    file_path = os.path.join(BASE_DIR, 'output', 'tables', 'table2.csv')
    df = pd.read_csv(file_path)
    assert df['Dataset'].isna().sum() == 0
    assert df['Dataset'].nunique() == df.shape[0]
    assert df.shape[0] == sum(df['Dataset'].map(lambda x: str(type(x)) == "<class 'str'>").tolist())
    assert df.select_dtypes(include=['float64', 'int64']).map(lambda x: x < 0).sum().sum() == 0
    
    
def test_content_table2():  
    '''Test if the numbers are correct within a tolerance level'''
    file_path = os.path.join(BASE_DIR, 'output', 'tables', 'table2.csv')
    df = pd.read_csv(file_path)
    original_table_results = {
        ('M1 Yearly', 'SES'): 4.938,
        ('M1 Quarterly', 'SES'): 1.929,
        ('M1 Monthly', 'SES'): 1.379,
        ('M3 Monthly', 'PR'): 1.010,
        ('Tourism Yearly', 'Deep AR'): 3.205,
        ('Weather', 'TBATS'): 0.689,
        ('NN5 Weekly', 'Theta'): 0.885,
    }
    for model_dataset, value in original_table_results.items():
        value_found = False
        if model_dataset[0] in df['Dataset'].values and model_dataset[1] in df.columns:
            replication_result = df.loc[df['Dataset'] == model_dataset[0], model_dataset[1]].values
            if replication_result:
                replication_result = replication_result[0]
                if replication_result in ['N/A', np.nan]:
                    continue
                if replication_result >= 0 or replication_result < 0:
                    assert round(replication_result, 3) / round(value, 3) <= 1.01
                    assert round(replication_result, 3) / round(value, 3) >= 0.99
                    value_found = True
        if not value_found:
            print(f"{model_dataset[0]}-{model_dataset[1]}: {value} not found in the replication table")


def test_all_content_table2():
    '''Test if all values are correct without considering the ones that should be different'''
    file_path = os.path.join(BASE_DIR, 'output', 'tables', 'table2.csv')
    df = pd.read_csv(file_path)
    test_df = df.set_index('Dataset')
    test_df = (
        test_df
        .drop(['Vehicle Trips', 'Rideshare', 'Bitcoin'])
        .drop(['Cat Boost', 'ARIMA'], axis=1) # We remove ARIMA because it is not in their final table
    )
    test_table1_paper_results = table2_paper_results.set_index('Dataset')
    expected_diff_results = {}
    for column in list(test_df.columns):
        comparison = (
            test_df[[column]].dropna(axis=0)
            .join(test_table1_paper_results[[column]], how='inner', lsuffix='_replication', rsuffix='_paper')
            .set_axis(['replication', 'paper'], axis=1)
            .assign(equal=lambda df: df.apply(lambda row: round(row['replication'], 3) == round(row['paper'], 3), axis=1))
        )
        if column in expected_diff_results.keys():
            comparison = comparison.drop(expected_diff_results[column])
        if column == 'TBATS':
            comparison.loc[lambda df: df.index.isin(['M4 Weekly', 'Sunspot'])] = (
                comparison.loc[lambda df: df.index.isin(['M4 Weekly', 'Sunspot'])]
                .assign(equal=lambda df: df.apply(lambda row: abs(round(row['replication'], 3) / round(row['paper'], 3) - 1) < .05, axis=1))
            )
        assert all(comparison.equal)


if __name__ == '__main__':
    test_generate_table2()
    test_logic_table2()
    test_content_table2()
    test_all_content_table2()