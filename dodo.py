"""
This script, utilizing the `doit` Python package, orchestrates a series of tasks for a time series analysis project.
It is structured to automate the entire workflow, from data acquisition and processing to statistical analysis and report generation.

Key functionalities include:

- Downloading time series datasets based on predefined URLs.
- Updating lists of selected models and datasets for analysis, which can be customized per run.
- Running statistical analysis scripts, including fixed horizon analysis with an R script.
- Generating statistical summary tables (Table 1 and Table 2) from the processed data.
- Transforming these tables into LaTeX format for inclusion in reports.
- Compiling the final report from LaTeX files, ensuring all results are up-to-date and formatted correctly.

Each task is defined with specific actions, dependencies, and triggers to ensure that only the necessary steps are rerun,
optimizing the workflow's efficiency. This setup allows for a modular and scalable approach to managing complex data analysis projects, facilitating easy updates and modifications to the analysis pipeline.
"""
import sys
sys.path.insert(1, './src/')


import config
from pathlib import Path
from doit.tools import run_once
from src.data_download import download_and_extract_zip
from src.data_download import URLS
from src.website_update_results import convert_tables_to_json
from src.tables_create import convert_tsf_to_dataframe
from src.tables_create import generate_table1_dataframe, generate_table2_dataframe
from src.tables_to_latex import upload_table_download_latex
from src.test_data_download import test_data_download

BASE_DIR = Path(config.BASE_DIR)
OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)

"""
The CHOSEN_MODELS specify which models will run when running doit.
If 'all' is set to True, all models will run.

The CHOSEN_DATASETS specify which datasets will be used when running doit.

If CHOSEN_MODELS is False for all values or CHOSEN_DATASETS is empty, the models will not run,
and the table will be generated with the current results.
"""

CHOSEN_MODELS = {
    'all': False, # All overrides the rest
    'arima': False,
    'catboost': False,
    'ets': False,
    'pooled_regression': False,
    'tbats': False,
    'ses': False,
    'theta': False,
    'dhr_arima': False,
}


CHOSEN_DATASETS = [
    'm1_yearly_dataset'
]

"""
The OTHER_ERROR_TABLES are the tables that generate other error metrics for the models.
"""


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
        chosen_models_list = [model for model, value in CHOSEN_MODELS.items() if value]
        chosen_models_list = ['all'] if 'all' in chosen_models_list else chosen_models_list
        for model in chosen_models_list:
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
        chosen_models_list = [model for model, value in CHOSEN_MODELS.items() if value]
        # Return True (up-to-date) if both lists are empty, False (not up-to-date) otherwise
        if chosen_models_list == [] or CHOSEN_DATASETS == []:
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
    def show_numeric_results(x):
        if not isinstance(x, (int, float)):
            return x
        if x < 1e2:
            return '{:.3f}'.format(x)
        elif x < 1e3:
            return '{:.0f}'.format(x)
        elif x < 1e6:
            x = x / 1e3
            return '{:.1f}K'.format(x)
        elif x < 1e9:
            x = x / 1e6
            return '{:.1f}M'.format(x)
        elif x < 1e12:
            x = x / 1e9
            return '{:.1f}B'.format(x)
        elif x < 1e15:
            x = x / 1e12
            return '{:.1f}T'.format(x)
        elif x < 1e18:
            x = x / 1e15
            return '{:.1f}Qa'.format(x)
        elif x >= 1e18:
            x = x / 1e15
            return '{:.1f}Qi'.format(x)
        return '{:.3f}'.format(x)

    for name in OTHER_ERROR_TABLES.keys():
        yield {
            'name': name,
            'actions': [(
                upload_table_download_latex,
                [f'output/tables/{name}.csv', name, lambda x: show_numeric_results(x), lambda x: '{:.2%}'.format(x), True]
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


def task_update_website_results():
    """Generate table1.csv from the downloaded data."""
    return {
        'actions': [convert_tables_to_json],
        'targets': [BASE_DIR / 'mtsr-web' / 'src' / 'Components' / 'test.json'],
        'uptodate': [False],
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