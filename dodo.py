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
from src.data_loader import convert_tsf_to_dataframe
from src.data_loader import generate_table1_dataframe
from src.test_data_download import test_data_download
from src.test_table1_csv import test_table1_results 

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
    for file, url in URLS.items():
        yield {
            'name': file,
            'actions': [(download_and_extract_zip, [url, DATA_DIR])],
            'targets': [DATA_DIR / file],  # Adjust as necessary
            'uptodate': [False],  # Force re-download every time, or adjust as necessary
            'clean': True,
        }

def task_generate_table1():
    yield {
        'name': 'Generate Table 1',
        'actions': [(generate_table1_dataframe, [DATA_DIR])],
        'targets': [BASE_DIR / 'results' / 'Table1.csv'],  # Adjust as necessary
        'uptodate': [False],  # Force re-download every time, or adjust as necessary
        'clean': True,
        'verbosity':0
    }