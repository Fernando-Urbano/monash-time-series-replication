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


# fmt: off
## Helper functions for automatic execution of Jupyter notebooks
def jupyter_execute_notebook(notebook):
    return f"jupyter nbconvert --execute --to notebook --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"

def jupyter_to_html(notebook, output_dir=OUTPUT_DIR):
    return f"jupyter nbconvert --to html --output-dir={output_dir} ./src/{notebook}.ipynb"

def jupyter_to_md(notebook, output_dir=OUTPUT_DIR):
    """Requires jupytext"""
    return f"jupytext --to markdown --output-dir={output_dir} ./src/{notebook}.ipynb"

def jupyter_to_python(notebook, build_dir):
    """Convert a notebook to a python script"""
    return f"jupyter nbconvert --to python ./src/{notebook}.ipynb --output _{notebook}.py --output-dir {build_dir}"

def jupyter_clear_output(notebook):
    return f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"


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


def task_transform_table2_to_latex():
    """Generate table1.csv from the downloaded data."""
    upload_table_download_latex_action = lambda x: upload_table_download_latex()
    return {
        'actions': [(upload_table_download_latex, ['output/tables/table2.csv', 'table2', lambda x: '{:.3f}'.format(x)])],
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
        'uptodate': [False],  # Force to generate table1 every time
        "clean": True,
    }