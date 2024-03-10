"""Run or update the project. This file uses the `doit` Python package. It works
like a Makefile, but is Python-based
"""
import sys
sys.path.insert(1, './src/')


import config
from pathlib import Path
from doit.tools import run_once
from src.data_download import download_and_extract_zip
from src.data_download import URLS
from src.tables_create import convert_tsf_to_dataframe
from src.tables_create import generate_table1_dataframe, generate_table2_dataframe
from src.tables_to_latex import upload_table_download_latex
from src.test_data_download import test_data_download

BASE_DIR = Path(config.BASE_DIR)
OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)

CHOSEN_MODELS = [
    # 'arima'
]


CHOSEN_DATASETS = [
    'm1_yearly_dataset'
]



OTHER_ERROR_TABLES = {
    'table_mean_smape': 'Mean SMAPE',
    'table_median_smape': 'Median SMAPE',
    'table_mean_smape': 'Mean mSMAPE',
    'table_median_mase': 'Median mSMAPE',
    'table_median_mase': 'Median MASE',
    'table_mean_mae': 'Mean MAE',
    'table_median_mae': 'Median MAE',
    'table_mean_rmse': 'Mean RMSE',
    'table_median_rmse': 'Median RMSE',
}


def update_chosen_models_and_datasets():
    """Update the chosen models and datasets"""
    with open('src/chosen_datasets.txt', 'w') as f:
        for dataset in CHOSEN_DATASETS:
            f.write(f'{dataset}\n')

    with open('src/chosen_models.txt', 'w') as f:
        for model in CHOSEN_MODELS:
            f.write(f'{model}\n')
    return True


def task_download_data():
    """Download the data from the source."""
    for file, url in URLS.items():
        yield {
            'name': file,
            'actions': [(download_and_extract_zip, [url, DATA_DIR])],
            'targets': [DATA_DIR / file],
            'uptodate': [True],  # Force re-download every time if equals to False
            'clean': True,
        }


def task_update_chosen_models_and_datasets():
    """Update the chosen models and datasets"""
    return {
        'actions': [update_chosen_models_and_datasets],
        'targets': ['src/chosen_models.txt', 'src/chosen_datasets.txt'],
        'uptodate': [False],
        'clean': True,
    }


def task_run_fixed_horizon_R_script():
    """Run the R script for fixed horizon analysis."""
    def run_if_lists_not_empty(task):
        # Return True (up-to-date) if both lists are empty, False (not up-to-date) otherwise
        if CHOSEN_MODELS == [] or CHOSEN_DATASETS == []:
            return True
        else:
            return False

    return {
        'actions': ['Rscript src/experiments/fixed_horizon.R'],  # Command to run the R script
        'uptodate': [run_if_lists_not_empty],
    }


def task_generate_table1():
    """Generate table1.csv from the downloaded data."""
    return {
        'actions': [(generate_table1_dataframe, [DATA_DIR])],
        'targets': [BASE_DIR / 'results' / 'tables' / 'table1.csv'],
        'uptodate': [False],  # Force re-download every time if equals to False
        'clean': True,
    }


def task_generate_table2():
    """Generate table2.csv from the downloaded data."""
    return {
        'actions': [(generate_table2_dataframe, ['Mean MASE'])],
        'targets': [BASE_DIR / 'results' / 'tables' / 'table2.csv'],
        'uptodate': [False],  # Force re-download every time if equals to False
        'clean': True,
        'verbosity': 0
    }


def task_generate_other_error_tables():
    """Generate table2.csv from the downloaded data."""
    for name, error_metric in OTHER_ERROR_TABLES.items():
        yield {
            'name': name,
            'actions': [(generate_table2_dataframe, [error_metric, name])],
            'targets': [BASE_DIR / 'results' / 'tables' / f'{name}.csv'],
            'uptodate': [False],  # Force re-download every time if equals to False
            'clean': True,
            'verbosity': 0
        }


def task_transform_table1_to_latex():
    """Generate table1.csv from the downloaded data."""
    return {
        'actions': [(upload_table_download_latex, ['output/tables/table1.csv', 'table1', lambda x: '{:.0f}'.format(x)])],
        "file_dep": [BASE_DIR / 'output' / 'tables' / 'table1.csv'],
        'targets': [BASE_DIR / 'output' / 'tables' / 'table1.tex'],
        'uptodate': [False],  # Force to generate table1 every time
        'clean': True,
        'verbosity': 0
    }


def task_transform_other_error_tables_to_latex():
    """Generate table1.csv from the downloaded data."""
    for name in OTHER_ERROR_TABLES.keys():
        yield {
            'name': name,
            'actions': [(
                upload_table_download_latex,
                [f'output/tables/{name}.csv', name, lambda x: '{:.3f}'.format(x), lambda x: '{:.2%}'.format(x), True]
            )],
            "file_dep": [BASE_DIR / 'output' / 'tables' / f'{name}.csv'],
            'targets': [BASE_DIR / 'output' / 'tables' / f'{name}.tex'],
            'uptodate': [False],  # Force to generate table2 every time
            'clean': True,
            'verbosity': 0
        }


def task_transform_table2_to_latex():
    """Generate table1.csv from the downloaded data."""
    return {
        'actions': [(
            upload_table_download_latex,
            ['output/tables/table2.csv', 'table2', lambda x: '{:.3f}'.format(x), lambda x: '{:.2%}'.format(x), True]
        )],
        "file_dep": [BASE_DIR / 'output' / 'tables' / 'table2.csv'],
        'targets': [BASE_DIR / 'output' / 'tables' / 'table2.tex'],
        'uptodate': [False],  # Force to generate table2 every time
        'clean': True,
        'verbosity': 0
    }


def task_compile_latex_docs():
    """Compiling the latex report"""
    return {
        "actions": [
            "latexmk -xelatex -cd ./reports/report.tex",  # Compile
            "latexmk -xelatex -c -cd ./reports/report.tex",  # Clean
        ],
        "targets": ["./reports/report.pdf"],
        "file_dep": ["./reports/report.tex"],
        'uptodate': [False],
        "clean": True,
    }