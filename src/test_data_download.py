import pandas as pd
import pytest
import os
try:
    from src.data_download import URLS
except:
    from data_download import URLS
from data_download import download_and_extract_zip

import config
from pathlib import Path

DATA_DIR = config.DATA_DIR


def test_data_download():
    tsf_files = [os.path.relpath(t) for t in list(Path(DATA_DIR).glob('*.tsf'))]
    assert len(tsf_files) == len(URLS.keys())


def test_specific_table_download():
    """
    Test downloading a specific table from a given URL and extracting it to the 'src' directory.
    """
    test_table = {
        'm1_yearly_dataset.tsf': 'https://zenodo.org/records/4656193/files/m1_yearly_dataset.zip?download=1'
    }
    download_and_extract_zip(list(test_table.values())[0], 'src')
    assert os.path.exists(os.path.join('src', 'm1_yearly_dataset.tsf'))
    os.remove(os.path.join('src', 'm1_yearly_dataset.tsf'))


if __name__ == '__main__':
    test_data_download()
    test_specific_table_download()