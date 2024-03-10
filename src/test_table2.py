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
        ('M1 Yearly', 'Cat Boost'): 4.427
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
    test_generate_table2()
    test_logic_table2()
    test_content_table2()