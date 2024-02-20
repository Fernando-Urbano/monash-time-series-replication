import pandas as pd
import pytest
import os
from src.data_download import URLS

import config
from pathlib import Path

DATA_DIR = config.DATA_DIR


def test_data_download():
    tsf_files = [os.path.relpath(t) for t in list(Path(DATA_DIR).glob('*.tsf'))]
    assert len(tsf_files) == len(URLS.keys())


if __name__ == '__main__':
    test_data_download()