import pandas as pd
import pytest
import os

import config
from pathlib import Path

DATA_DIR = config.DATA_DIR
BASE_DIR = config.BASE_DIR

def test_table1_results():
    file_path = os.path.join(BASE_DIR, 'results', 'table1.csv')

    if os.path.exists(file_path):
        print('----Check results folder for Table1.csv file----')
        assert True
    else:
        assert False


if __name__ == '__main__':
    # Test
    test_table1_results()