from datetime import datetime
from distutils.util import strtobool

import pandas as pd
import os
import config

import re
from pathlib import Path

BASE_DIR = Path(config.BASE_DIR)
OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)


DATASETS_TO_IGNORE = [
    'Bitcoin', 'Sunspot'
]


def convert_tables_to_json():
    csv_tables = [t for t in os.listdir(BASE_DIR / 'output' / 'tables') if t.endswith('.csv') and t != 'table1.csv']
    error_metric_results = {}
    for table_name in csv_tables:
        try:
            table = pd.read_csv(BASE_DIR / 'output' / 'tables' / table_name)
            if 'Dataset' in list(table.columns):
                table = table.set_index('Dataset')
            table = table.loc[lambda df: [d for d in df.index if d not in DATASETS_TO_IGNORE]]
            if '(DHR-) ARIMA' in list(table.columns):
                table = table.rename({'(DHR-) ARIMA': 'DHR-ARIMA'}, axis=1)
            dict_result = table.to_dict()
            dict_result = {
                model: {
                    dataset: round(value, 3) for dataset, value in results.items() if isinstance(value, float) and value > 0
                }
                for model, results in dict_result.items()
            }
            if table_name == 'table2.csv':
                error_metric = 'Mean MASE'
            else:
                error_metric = (
                    table_name
                    .replace('table_', '')
                    .replace('.csv', '')
                    .replace('_', ' ')
                    .upper()
                    .replace('MEAN', 'Mean')
                    .replace('MEDIAN', 'Median')
                )
            error_metric_results[error_metric] = dict_result
        except Exception as e:
            print(f'Error in {table_name}: {str(e)[:100]}')
        with open(BASE_DIR / 'mtsr-web' / 'src' / 'Components' / 'test.json', 'w') as f:
            f.write(str(error_metric_results).replace("'", '"'))


if __name__ == '__main__':
    convert_tables_to_json()