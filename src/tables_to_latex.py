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
        ptc_format_func,
        float_format_func,
        pct_columns=None
):
    df = df.copy()
    if pct_columns is None:
        pct_columns = []
    number_columns = df.select_dtypes(include=['float64', 'int']).columns
    float_columns = [n for n in number_columns if n not in pct_columns]
    pct_columns = [n for n in number_columns if n in pct_columns]
    df[float_columns] = df[float_columns].applymap(float_format_func)
    df[pct_columns] = df[pct_columns].applymap(ptc_format_func)
    return df.to_latex()


def upload_table_download_latex(
        input_path,
        table_name,
        output_path=OUTPUT_DIR / 'tables',
        ptc_format_func=lambda x: '{:.2f}'.format(x),
        float_format_func=lambda x: '{:.4f}'.format(x),
        pct_columns=None,
    ):
    df = pd.read_csv(input_path)
    latex_table_string = convert_table_to_latex(df, ptc_format_func, float_format_func, pct_columns)
    path = output_path / f'{table_name}.tex'
    with open(path, "w") as text_file:
        text_file.write(latex_table_string)


if __name__ == '__main__':
    # Example Generate Table 1
    upload_table_download_latex('output/tables/table1.csv', 'table1')

