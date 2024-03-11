'''
This script is a collection of tests designed to ensure the accuracy and structural integrity of 'table1.csv', a key data file in the project.
The tests are as follows:

- `test_generate_table1` verifies the existence of 'table1.csv' in the expected directory.
- `test_format_table1` confirms that 'table1.csv' contains the correct number of rows and a permissible range of columns, as well as checks
for the presence of specific expected column headers.
- `test_logic_table1` ensures logical consistency within the data, such as the minimum length of time series not exceeding the maximum length,
and the number of frequencies and series being greater than zero.
- `test_content_table1` compares selected values from 'table1.csv' against predefined correct values, within a narrow margin of tolerance,
to confirm the accuracy of key data points.

When executed, these tests will automatically perform the validations and raise errors if any discrepancies are found,
thus serving as an automated data validation tool for the table. This is crucial for maintaining data quality and can be especially helpful
after any updates or changes to the underlying data processing steps.
'''
import pandas as pd
import pytest
import os
import numpy as np

import config
from pathlib import Path

DATA_DIR = config.DATA_DIR
BASE_DIR = config.BASE_DIR

table1_paper_results = pd.DataFrame({
    'Dataset': [
        'M1', 'M3', 'M4', 'Tourism', 'CIF 2016', 'London Smart Meters', 'Aus. Electricity Demand', 
        'Wind Farms', 'Dominick', 'Bitcoin', 'Pedestrian Counts', 'Vehicle Trips', 'KDD Cup 2018', 
        'Weather', 'NN5', 'Web Traffic', 'Solar', 'Electricity', 'Car Parts', 'FRED-MD', 
        'San Francisco Traffic', 'Rideshare', 'Hospital', 'COVID Deaths', 'Temperature Rain', 
        'Sunspot', 'Saugeen River Flow', 'US Births', 'Solar Power', 'Wind Power'
    ],
    'Domain': [
        'Multiple', 'Multiple', 'Multiple', 'Tourism', 'Banking', 'Energy', 'Energy', 'Energy', 
        'Sales', 'Economic', 'Transport', 'Transport', 'Nature', 'Nature', 'Banking', 'Web', 
        'Energy', 'Energy', 'Sales', 'Economic', 'Transport', 'Transport', 'Health', 'Nature', 
        'Nature', 'Nature', 'Nature', 'Nature', 'Energy', 'Energy'
    ],
    'No: of Series': [
        1001, 3003, 100000, 1311, 72, 5560, 5, 339, 115704, 18, 66, 329, 270, 3010, 111, 
        145063, 137, 321, 2674, 107, 862, 2304, 767, 266, 32072, 1, 1, 1, 1, 1
    ],
    'Min. Length': [
        15, 20, 19, 11, 34, 288, 230736, 6345, 28, 2659, 576, 70, 9504, 1332, 791, 803, 
        52560, 26304, 51, 728, 17544, 541, 84, 212, 725, 73931, 23741, 7305, 7397222, 7397147
    ],
    'Max. Length': [
        150, 144, 9933, 333, 120, 39648, 232272, 527040, 393, 4581, 96424, 243, 10920, 65981, 
        791, 803, 52560, 26304, 51, 728, 17544, 541, 84, 212, 725, 73931, 23741, 7305, 7397222, 
        7397147
    ],
    'No: of Freq': [3, 4, 6, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'Missing': [
        'No', 'No', 'No', 'No', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'No', 'Yes',
        'Yes', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'Yes', 'No', 'No', 'No', 'No'
    ],
    'Competition': [
        'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'Yes', 'No', 'Yes', 
        'Yes', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No'
    ],
    'Multivariate': [
        'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 
        'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No', 'No', 'No', 'No', 'No'
    ]
})

def test_generate_table1():
    '''Test if table1 exists in the output directory. It already gives an idea if the problem in other tests is due to that'''
    file_path = os.path.join(BASE_DIR, 'output', 'tables', 'table1.csv')
    assert os.path.exists(file_path)


def test_format_table1():
    '''Test if the format of table 1 is as expected'''
    file_path = os.path.join(BASE_DIR, 'output', 'tables', 'table1.csv')
    df = pd.read_csv(file_path)
    assert df.shape[0] == 30
    assert df.shape[1] in [9, 10]
    columns = [
        'Dataset', 'Domain', 'No: of Series', 'Min. Length',
        'Max. Length', 'No: of Freq',
        'Missing', 'Competition', 'Multivariate'
    ]
    assert sum([1 for c in df.columns if c not in columns]) == 0


def test_logic_table1():
    '''Test if the numbers make sense'''
    file_path = os.path.join(BASE_DIR, 'output', 'tables', 'table1.csv')
    df = pd.read_csv(file_path)
    assert all(df['Min. Length'] <= df['Max. Length'])
    assert all(df['No: of Freq'] > 0)
    assert all(df['No: of Series'] > 0)


def test_content_table1():  
    '''Test if the numbers are correct within a tolerance level'''
    file_path = os.path.join(BASE_DIR, 'output', 'tables', 'table1.csv')
    df = pd.read_csv(file_path)
    original_table_results = {
        ('M1', 'Max. Length'): 150,
        ('M3', 'Min. Length'): 20,
        ('Web Traffic', 'No: of Series'): 145063,
        ('Temperature Rain', 'No: of Series'): 32072,
        ('Sunspot', 'Max Length'): 73931,
    }
    for model_dataset, value in original_table_results.items():
        if model_dataset[0] in df['Dataset'].values and model_dataset[1] in df.columns:
            replication_result = df.loc[df['Dataset'] == model_dataset[0], model_dataset[1]].values
            if replication_result:
                replication_result = replication_result[0]
                if replication_result in ['N/A', np.nan]:
                    continue
                assert round(replication_result, 3) / round(value, 3) <= 1.01
                assert round(replication_result, 3) / round(value, 3) >= 0.99


def test_all_content_table1():
    '''Test if all values are correct without considering the ones that should be different'''
    file_path = os.path.join(BASE_DIR, 'output', 'tables', 'table1.csv')
    df = pd.read_csv(file_path)
    test_df = df.set_index('Dataset')
    test_table1_paper_results = table1_paper_results.set_index('Dataset')
    expected_diff_results = {
        'No: of Series': 'M1',
        'Min. Length': ['Sunspot', 'Bitcoin', 'M1', 'CIF 2016'],
        'Max. Length': ['Sunspot'],

    }
    for column in list(test_df.columns):
        comparison = (
            pd.concat([test_df[column], test_table1_paper_results[column]], axis=1)
            .set_axis(['replication', 'paper'], axis=1)
            .assign(equal=lambda df: df.apply(lambda row: row['replication'] == row['paper'], axis=1))
        )
        if column in expected_diff_results.keys():
            comparison = comparison.drop(expected_diff_results[column])
        assert all(comparison.equal)



if __name__ == '__main__':
    test_generate_table1()
    test_format_table1()
    test_logic_table1()
    test_content_table1()
    test_all_content_table1()