r"""
You can test out the latex code in the following minimal working
example document:

\documentclass{article}
\usepackage{booktabs}
\begin{document}
First document. This is a simple example, with no 
extra parameters or packages included.

\begin{table}
\centering
YOUR LATEX TABLE CODE HERE
%\input{example_table.tex}
\end{table}
\end{document}

"""
import pandas as pd
import numpy as np
np.random.seed(100)

import config
from pathlib import Path
DATA_DIR = Path(config.DATA_DIR)
OUTPUT_DIR = Path(config.OUTPUT_DIR)


## Suppress scientific notation and limit to 3 decimal places
# Sets display, but doesn't affect formatting to LaTeX
# pd.set_option('display.float_format', lambda x: '%.2f' % x)
# Sets format for printing to LaTeX
# float_format_func = lambda x: '{:.2f}'.format(x)


def convert_table_to_latex(
        df,
        float_format_func,
        ptc_format_func,
        highlight_min_row=False,
        specific_columns_func=None,
        pct_columns=None
):
    """
    Converts a DataFrame into a LaTeX table string.

    Args:
        df (DataFrame): Input DataFrame to convert.
        float_format_func (function): Function to format float columns.
        ptc_format_func (function): Function to format percentage columns.
        highlight_min_row (bool): Flag to highlight the minimum value in each row.
        specific_columns_func (dict): Functions specified for specific columns.
        pct_columns (list): Columns considered as percentage values.

    Returns:
        str: LaTeX table string.
    """    
    df = df.copy()
    if pct_columns is None:
        pct_columns = []
    number_columns = df.select_dtypes(include=['float64', 'int']).columns
    if highlight_min_row:
        min_columns = {}
        for i in range(len(df.index)):
            try:
                min_columns[i] = df.iloc[i].loc[number_columns].idxmin()
            except:
                pass
    if specific_columns_func:
        for column, func in specific_columns_func.items():
            df[column] = df[column].apply(func)
        number_columns = [n for n in number_columns if n not in specific_columns_func.keys()]
    float_columns = [n for n in number_columns if n not in pct_columns]
    pct_columns = [n for n in number_columns if n in pct_columns]
    df[float_columns] = df[float_columns].map(float_format_func)
    df[pct_columns] = df[pct_columns].map(ptc_format_func)
    if highlight_min_row:
        for i in range(len(df.index)):
            if i in min_columns.keys():
                if str(min_columns[i]) != 'nan':
                    df[min_columns[i]].iloc[i] = '\\textbf{' + df.iloc[i].loc[min_columns[i]] + '}'
    df = df.map(lambda x: x.replace('nan', '-'))
    return df.to_latex()


def upload_table_download_latex(
        input_path,
        table_name,
        float_format_func=lambda x: '{:.4f}'.format(x),
        ptc_format_func=lambda x: '{:.2f}'.format(x),
        highlight_min_row=False,
        specific_columns_func=None,
        output_path=OUTPUT_DIR / 'tables',
        pct_columns=None,
    ):
    """
    Uploads a table, converts it to LaTeX, and saves the LaTeX file.

    Args:
        input_path (str): Path to the input CSV file.
        table_name (str): Name for the output LaTeX table file.
        float_format_func (function): Function to format float columns.
        ptc_format_func (function): Function to format percentage columns.
        highlight_min_row (bool): Flag to highlight the minimum value in each row.
        specific_columns_func (dict): Functions specified for specific columns.
        output_path (Path): Path to save the output LaTeX file.
        pct_columns (list): Columns considered as percentage values.
    """    
    df = pd.read_csv(input_path)
    latex_table_string = convert_table_to_latex(df, float_format_func, ptc_format_func, highlight_min_row, pct_columns, specific_columns_func)
    path = output_path / f'{table_name}.tex'
    with open(path, "w") as text_file:
        text_file.write(latex_table_string)


if __name__ == '__main__':
    # Example Generate Table 1
    upload_table_download_latex('output/tables/table_median_smape.csv', 'table_median_smape', highlight_min_row=True)
    # upload_table_download_latex('output/tables/table2.csv', 'table2', highlight_min_row=True)
    # upload_table_download_latex('output/tables/table1.csv', 'table1')

