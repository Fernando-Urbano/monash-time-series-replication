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

def test_generate_table2():
    file_path = os.path.join(BASE_DIR, 'output', 'tables', 'table2.csv')
    assert os.path.exists(file_path)


def test_logic_table2():
    file_path = os.path.join(BASE_DIR, 'output', 'tables', 'table2.csv')
    df = pd.read_csv(file_path)
    assert df['Dataset'].isna().sum() == 0
    assert df['Dataset'].nunique() == df.shape[0]
    assert df.shape[0] == sum(df['Dataset'].map(lambda x: str(type(x)) == "<class 'str'>").tolist())
    assert df.select_dtypes(include=['float64', 'int64']).map(lambda x: x < 0).sum().sum() == 0
    
    
def test_content_table2():  
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


if __name__ == '__main__':
    test_generate_table2()
    test_logic_table2()
    test_content_table2()