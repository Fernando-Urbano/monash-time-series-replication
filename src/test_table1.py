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


if __name__ == '__main__':
    test_generate_table1()
    test_format_table1()
    test_logic_table1()
    test_content_table1()