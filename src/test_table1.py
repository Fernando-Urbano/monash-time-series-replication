import pandas as pd
import pytest
import os

import config
from pathlib import Path

DATA_DIR = config.DATA_DIR
BASE_DIR = config.BASE_DIR

def test_generate_table1():
    file_path = os.path.join(BASE_DIR, 'results', 'table1.csv')
    assert os.path.exists(file_path)


def test_format_table1():
    file_path = os.path.join(BASE_DIR, 'results', 'table1.csv')
    df = pd.read_csv(file_path)
    assert df.shape[0] == 30
    assert df.shape[1] == 9
    assert df.columns.tolist() == [
        'Domain', 'No: of Series', 'Min. Length',
        'Max. Length', 'No: of Freq',
        'Missing', 'Competition', 'Multivariate'
    ]


def test_logic_table1():
    file_path = os.path.join(BASE_DIR, 'results', 'table1.csv')
    df = pd.read_csv(file_path)
    assert all(df['Min. Length'] <= df['Max. Length'])
    assert all(df['No: of Freq'] > 0)
    assert all(df['No: of Series'] > 0)


if __name__ == '__main__':
    test_generate_table1()
    test_format_table1()
    test_logic_table1()