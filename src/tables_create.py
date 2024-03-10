'''
For Table 1, the script features a function to convert Time Series Forecasting (TSF) files into pandas DataFrames,
accommodating missing values and varying series lengths.
It compiles the information of multiple datasets, such as the number of series, the length of series, frequency, and the presence of missing values, among others.
This data is then organized into a DataFrame and saved in both CSV and Excel formats.

For Table 2, the script processes the error metric results for different forecasting models across datasets.
It reads result files, converts them into a structured format, and then pivots the data for easier comparison and visualization.
The resulting DataFrame is also saved in CSV and Excel formats.
'''
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

def convert_tsf_to_dataframe(
    full_file_path_and_name,
    replace_missing_vals_with="NaN",
    value_column_name="series_value",
):
    """
    Converts a Time Series Forecasting (TSF) file into a pandas DataFrame.

    Parameters:
    - full_file_path_and_name (str): The complete path and filename of the TSF file to be read.
    - replace_missing_vals_with (str, optional): The value used to replace missing values in the series. Defaults to "NaN".
    - value_column_name (str, optional): The name to be used for the column that will contain the series values. Defaults to "series_value".

    Returns:
    - tuple: A tuple containing the loaded DataFrame, frequency of the dataset, forecast horizon, flags indicating if the dataset contains missing values, if all series are of equal length, and if the dataset is for a competition.
    """    
    col_names = []
    col_types = []
    all_data = {}
    line_count = 0
    competition_dataset = False
    frequency = None
    forecast_horizon = None
    contain_missing_values = None
    contain_equal_length = None
    found_data_tag = False
    found_data_section = False
    started_reading_data_section = False

    with open(full_file_path_and_name, "r", encoding="cp1252") as file:
        for line in file:
            # Strip white space from start/end of line
            line = line.strip()

            if line:
                if line.startswith("#"):
                    if 'competition' in line or 'Competition' in line:
                        competition_dataset=True

                if line.startswith("@"):  # Read meta-data
                    if not line.startswith("@data"):
                        line_content = line.split(" ")
                        if line.startswith("@attribute"):
                            if (
                                len(line_content) != 3
                            ):  # Attributes have both name and type
                                raise Exception("Invalid meta-data specification.")

                            col_names.append(line_content[1])
                            col_types.append(line_content[2])
                        else:
                            if (
                                len(line_content) != 2
                            ):  # Other meta-data have only values
                                raise Exception("Invalid meta-data specification.")

                            if line.startswith("@frequency"):
                                frequency = line_content[1]
                            elif line.startswith("@horizon"):
                                forecast_horizon = int(line_content[1])
                            elif line.startswith("@missing"):
                                contain_missing_values = bool(
                                    strtobool(line_content[1])
                                )
                            elif line.startswith("@equallength"):
                                contain_equal_length = bool(strtobool(line_content[1]))

                    else:
                        if len(col_names) == 0:
                            raise Exception(
                                "Missing attribute section. Attribute section must come before data."
                            )

                        found_data_tag = True
                elif not line.startswith("#"):
                    if len(col_names) == 0:
                        raise Exception(
                            "Missing attribute section. Attribute section must come before data."
                        )
                    elif not found_data_tag:
                        raise Exception("Missing @data tag.")
                    else:
                        if not started_reading_data_section:
                            started_reading_data_section = True
                            found_data_section = True
                            all_series = []

                            for col in col_names:
                                all_data[col] = []

                        full_info = line.split(":")

                        if len(full_info) != (len(col_names) + 1):
                            raise Exception("Missing attributes/values in series.")

                        series = full_info[len(full_info) - 1]
                        series = series.split(",")

                        if len(series) == 0:
                            raise Exception(
                                "A given series should contains a set of comma separated numeric values. At least one numeric value should be there in a series. Missing values should be indicated with ? symbol"
                            )

                        numeric_series = []

                        for val in series:
                            if val == "?":
                                numeric_series.append(replace_missing_vals_with)
                            else:
                                numeric_series.append(float(val))

                        if numeric_series.count(replace_missing_vals_with) == len(
                            numeric_series
                        ):
                            raise Exception(
                                "All series values are missing. A given series should contains a set of comma separated numeric values. At least one numeric value should be there in a series."
                            )

                        all_series.append(pd.Series(numeric_series).array)

                        for i in range(len(col_names)):
                            att_val = None
                            if col_types[i] == "numeric":
                                att_val = int(full_info[i])
                            elif col_types[i] == "string":
                                att_val = str(full_info[i])
                            elif col_types[i] == "date":
                                att_val = datetime.strptime(
                                    full_info[i], "%Y-%m-%d %H-%M-%S"
                                )
                            else:
                                raise Exception(
                                    "Invalid attribute type."
                                )  # Currently, the code supports only numeric, string and date types. Extend this as required.

                            if att_val is None:
                                raise Exception("Invalid attribute value.")
                            else:
                                all_data[col_names[i]].append(att_val)

                line_count = line_count + 1

        if line_count == 0:
            raise Exception("Empty file.")
        if len(col_names) == 0:
            raise Exception("Missing attribute section.")
        if not found_data_section:
            raise Exception("Missing series information under data section.")

        all_data[value_column_name] = all_series
        loaded_data = pd.DataFrame(all_data)

        return (
            loaded_data,
            frequency,
            forecast_horizon,
            contain_missing_values,
            contain_equal_length,
            competition_dataset,
        )

DATASETS_TO_INFO = {
    'M1': {
        'Domain': 'Multiple',
        'Datasets': [
            'm1_monthly_dataset.tsf',
            'm1_quarterly_dataset.tsf',
            'm1_quarterly_dataset.tsf'
        ],
        'Multivariate': False
    },
    'M3': {
        'Domain': 'Multiple',
        'Datasets': [
            'm3_monthly_dataset.tsf',
            'm3_quarterly_dataset.tsf',
            'm3_yearly_dataset.tsf',
            'm3_other_dataset.tsf'
        ],
        'Multivariate': False
    },
    'M4': {
        'Domain': 'Multiple',
        'Datasets': [
            'm4_monthly_dataset.tsf',
            'm4_quarterly_dataset.tsf',
            'm4_yearly_dataset.tsf',
            'm4_weekly_dataset.tsf',
            'm4_daily_dataset.tsf',
            'm4_hourly_dataset.tsf'
        ],
        'Multivariate': False
    },
    'Tourism': {
        'Domain': 'Tourism',
        'Datasets': [
            'tourism_monthly_dataset.tsf',
            'tourism_quarterly_dataset.tsf',
            'tourism_yearly_dataset.tsf'
        ],
        'Multivariate': False
    },
    'CIF 2016': {
        'Domain': 'Banking',
        'Datasets': [
            'cif_2016_dataset.tsf'
        ],
        'Multivariate': False
    },
    'London Smart Meters': {
        'Domain': 'Energy',
        'Datasets': [
            'london_smart_meters_dataset_with_missing_values.tsf',
        ],
        'Multivariate': False
    },
    'Aus. Electricity Demand': {
        'Domain': 'Energy',
        'Datasets': [
            'australian_electricity_demand_dataset.tsf'
        ],
        'Multivariate': False
    },
    'Wind Farms': {
        'Domain': 'Energy',
        'Datasets': [
            'wind_farms_minutely_dataset_with_missing_values.tsf',
        ],
        'Multivariate': False
    },
    'Dominick': {
        'Domain': 'Sales',
        'Datasets': [
            'dominick_dataset.tsf'
        ],
        'Multivariate': False
    },
    'Bitcoin': {
        'Domain': 'Economic',
        'Datasets': [
            'bitcoin_dataset_with_missing_values.tsf'
        ],
        'Multivariate': False
    },
    'Pedestrian Counts': {
        'Domain': 'Transport',
        'Datasets': [
            'pedestrian_counts_dataset.tsf'
        ],
        'Multivariate': False
    },
    'Vehicle Trips': {
        'Domain': 'Transport',
        'Datasets': [
            'vehicle_trips_dataset_with_missing_values.tsf'
        ],
        'Multivariate': False
    },
    'KDD Cup 2018': {
        'Domain': 'Transport',
        'Datasets': [
            'kdd_cup_2018_dataset_with_missing_values.tsf'
        ],
        'Multivariate': False
    },
    'Weather': {
        'Domain': 'Weather',
        'Datasets': [
            'weather_dataset.tsf'
        ],
        'Multivariate': False
    },
    'NN5': {
        'Domain': 'Banking',
        'Datasets': [
            'nn5_daily_dataset_with_missing_values.tsf',
            'nn5_weekly_dataset.tsf'
        ],
        'Multivariate': True
    },
    'Web Traffic': {
        'Domain': 'Web',
        'Datasets': [
            'kaggle_web_traffic_dataset_with_missing_values.tsf'
        ],
        'Multivariate': True
    },
    'Solar': {
        'Domain': 'Energy',
        'Datasets': [
            'solar_10_minutes_dataset.tsf',
            'solar_weekly_dataset.tsf'
        ],
        'Multivariate': True
    },
    'Electricity': {
        'Domain': 'Energy',
        'Datasets': [
            'electricity_hourly_dataset.tsf',
            'electricity_weekly_dataset.tsf'
        ],
        'Multivariate': True
    },
    'Car Parts': {
        'Domain': 'Sales',
        'Datasets': [
            'car_parts_dataset_with_missing_values.tsf'
        ],
        'Multivariate': True
    },
    'FRED-MD': {
        'Domain': 'Economics',
        'Datasets': [
            'fred_md_dataset.tsf'
        ],
        'Multivariate': True
    },
    'San Francisco Traffic': {
        'Domain': 'Transport',
        'Datasets': [
            'traffic_hourly_dataset.tsf',
            'traffic_weekly_dataset.tsf'
        ],
        'Multivariate': True
    },
    'Rideshare': {
        'Domain': 'Transport',
        'Datasets': [
            'rideshare_dataset_with_missing_values.tsf'
        ],
        'Multivariate': True
    },
    'Hospital': {
        'Domain': 'Health',
        'Datasets': [
            'hospital_dataset.tsf'
        ],
        'Multivariate': True
    },
    'COVID Deaths': {
        'Domain': 'Nature',
        'Datasets': [
            'covid_deaths_dataset.tsf'
        ],
        'Multivariate': True
    },
    'Temperature Rain': {
        'Domain': 'Nature',
        'Datasets': [
            'temperature_rain_dataset_with_missing_values.tsf'
        ],
        'Multivariate': True
    },
    'Sunspot': {
        'Domain': 'Nature',
        'Datasets': [
            'sunspot_dataset_with_missing_values.tsf'
        ],
        'Multivariate': False
    },
    'Saugeen River Flow': {
        'Domain': 'Nature',
        'Datasets': [
            'saugeenday_dataset.tsf'
        ],
        'Multivariate': False
    },
    'US Births': {
        'Domain': 'Nature',
        'Datasets': [
            'us_births_dataset.tsf'
        ],
        'Multivariate': False
    },
    'Solar Power': {
        'Domain': 'Energy',
        'Datasets': [
            'solar_4_seconds_dataset.tsf'
        ],
        'Multivariate': False
    },
    'Wind Power': {
        'Domain': 'Energy',
        'Datasets': [
            'wind_4_seconds_dataset.tsf'
        ],
        'Multivariate': False
    },
}


def generate_single_dataset_info(dataset_name, dataset_information):
    dataset_statistics = {
        'Domain': dataset_information['Domain'],
        'No: of Series': 0,
        'Min. Length': 1e10,
        'Max. Length': 0,
        'No: of Freq': len(dataset_information['Datasets']),
        'Missing': None,
        'Competition': None,
        'Multivariate': dataset_information['Multivariate']
    }
    """
    Generates statistics for a single dataset based on the dataset information provided.

    This function iterates through the datasets contained within the dataset_information
    dictionary, computes various statistics such as minimum and maximum series length,
    and aggregates information like the total number of series and whether the dataset
    contains missing values or is part of a competition.

    Parameters:
    - dataset_name (str): The name of the dataset being analyzed.
    - dataset_information (dict): A dictionary containing metadata about the dataset,
      including the domain, whether it's multivariate, and the list of dataset file names.

    Returns:
    - dict: A dictionary containing the computed statistics for the dataset, including
      the domain, total number of series, minimum and maximum series length, number of
      frequencies, presence of missing values, whether it's part of a competition, and
      whether it's multivariate.
    """    
    if len(dataset_information['Datasets']) > 1:
        if dataset_name not in ['M4']:
            dataset_information['Datasets'] = [d for d in dataset_information['Datasets'] if not bool(re.search('_weekly_', d))]
    for dataset in dataset_information['Datasets']:
        loaded_data, frequency, forecast_horizon, contain_missing_values, contain_equal_length, competition_dataset = convert_tsf_to_dataframe(str(DATA_DIR) + '/' + dataset)
        loaded_data['len_series'] = loaded_data['series_value'].apply(lambda x: len(x))
        min_len = loaded_data['len_series'].min()
        max_len = loaded_data['len_series'].max()
        dataset_statistics['Min. Length'] = min_len if min_len < dataset_statistics['Min. Length'] else dataset_statistics['Min. Length']
        dataset_statistics['Max. Length'] = max_len if max_len > dataset_statistics['Max. Length'] else dataset_statistics['Max. Length']
        dataset_statistics['No: of Series'] += loaded_data.shape[0] if dataset not in ['traffic_weekly_dataset.tsf'] else 0
        if dataset_statistics['Missing'] is None:
            dataset_statistics['Missing'] = contain_missing_values
        if dataset_statistics['Competition'] is None:
            dataset_statistics['Competition'] = competition_dataset
    return dataset_statistics


def generate_table1_dataframe(print_dataset_name=False):
    """
    Generates a DataFrame summarizing the statistics of multiple datasets and saves it to CSV and Excel files.

    Loops through each dataset mentioned in the 'DATASETS_TO_INFO' global dictionary to compile
    statistics using the 'generate_single_dataset_info' function. Manages exceptions encountered
    during data gathering, displays dataset names upon request, and arranges the resulting DataFrame.
    Finally, stores the data as CSV and Excel files in a specified directory.

    Parameters:
    - print_dataset_name (bool, optional): If True, prints the name of each dataset being processed.
      Defaults to False.

    Returns:
    - bool: True if the function executes successfully, indicating the DataFrame has been generated
      and saved.
    """
    datasets_statistics = {}
    for dataset_name, dataset_info in DATASETS_TO_INFO.items():
        if print_dataset_name:
            print(dataset_name)
        try:
            datasets_statistics[dataset_name] = generate_single_dataset_info(dataset_name, dataset_info)
        except Exception as e:
            e = str(e) if len(str(e)) < 100 else str(e)[:50] + "... [truncated]"
            print(f'Error in {dataset_name}: {e}')
    df_table1 = (
        pd.DataFrame(datasets_statistics)
        .transpose()
        .reset_index()
        .rename({'index': 'Dataset'}, axis=1)
    )
    bool_columns = ['Missing', 'Competition', 'Multivariate']
    df_table1[bool_columns] = df_table1[bool_columns].map(lambda x: 'Yes' if x else 'No')
    csv_file_path = os.path.join(BASE_DIR, 'output', 'tables', 'table1.csv')
    results_folder = os.path.join(BASE_DIR, 'output', 'tables')
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    df_table1.reset_index(drop=True, inplace=True)
    df_table1.to_csv(csv_file_path, index=False)
    df_table1.to_excel(csv_file_path.replace('.csv', '.xlsx'), index=False)
    return True


def transform_string_results_to_dict(results_list):
    """
    Converts a list of string results into a dictionary.

    Parses each string in the input list, separating the key and value by ':'. Keys are
    trimmed and added as dictionary keys. Values are converted to floats unless 'NA' is
    indicated, in which case the value is set to None.

    Parameters:
    - results_list (list): List of strings formatted as "key: value".

    Returns:
    - dict: A dictionary with keys and corresponding values derived from the input list.
    """    
    results_dict = {}
    for result in results_list:
        parts = result.split(':')
        if len(parts) == 1:
            continue
        key = parts[0].strip()
        if parts[1].strip().lower()[:2] == 'na':
            value = None
        else:
            value = float(parts[1].strip())
        results_dict[key] = value
    return results_dict


ORDER_MODELS = [
    'SES', 'Theta', 'ETS', '(DHR-) ARIMA', 'PR',
    'Cat Boost', 'FFNN', 'Deep AR', 'N-BEATS', 'Wave Net', 'Transformer'
]

ORDER_DATASETS = [
    'M1 Yearly', 'M1 Quarterly', 'M1 Monthly', 'M3 Quarterly',
    'M3 Monthly', 'M3 Other', 'M4 Yearly', 'M4 Quarterly',
    'M4 Monthly', 'M4 Weekly', 'M4 Daily', 'M4 Hourly', 'Tourism Yearly',
    'Tourism Quarterly', 'Tourism Monthly', 'Aus. Elecdemand', 'Dominick',
    ' Bitcoin', 'Pedestrians', 'Vehicle Trips', 'Weather', 'NN5 Daily',
    'NN5 Weekly', 'Kaggle Daily', 'Kaggle Weekly', 'Solar 10 Mins',
    'Solar Weekly', 'Electricity Hourly', 'Electricity Weekly', 'Carparts',
    'FRED-MD', 'Traffic Hourly', 'Traffic Weekly', 'Rideshare', 'Hospital',
    'COVID', 'Temp. Rain', 'Sunspot', 'Saugeen', 'Births'
]


MODEL_PATTERN_TO_NAME = {
    '_pooled_regression': 'PR',
    '_catboost': 'Cat Boost',
    '_theta[.]': 'Theta',
    '_ets[.]': 'ETS',
    '_tbats[.]': 'TBATS',
    '_ses[.]': 'SES',
    '_dhr_arima': '(DHR-) ARIMA',
    '_arima[.]': 'ARIMA',
}


DATABASE_NAMES_EXCEPTIONS = {
    'covid_deaths': 'covid',
}


def get_model_name(name):
    """
    Maps a given name to a predefined model name based on matching patterns.

    Args:
        name (str): The name to match against predefined patterns.

    Returns:
        str: The matched model name from MODEL_PATTERN_TO_NAME.
        
    Raises:
        Exception: If the name doesn't match any predefined patterns.
    """   
    for pattern, model in MODEL_PATTERN_TO_NAME.items():
        if re.search(pattern, name):
            return model
    else:
        raise Exception('Unrecognized model name: add it to "MODEL_PATTERN_TO_NAME" dictionary')

def get_database_name(name):
    """
    Extracts and formats the database name from a given string based on known patterns.
    
    Args:
        name (str): The name containing the database identifier.
    
    Returns:
        str: A human-readable, formatted database name.
    """    
    for pattern in MODEL_PATTERN_TO_NAME.keys():
        if re.search(pattern, name):
            pattern = pattern.replace('[.]', '.')
            database_pattern = name.split(pattern)[0]
            break
    pattern = DATABASE_NAMES_EXCEPTIONS[pattern] if pattern in DATABASE_NAMES_EXCEPTIONS else pattern
    database_title = database_pattern.replace('_', ' ').title()
    uppercase_word = ['M1', 'M3', 'M4', 'CIF', 'NN5', 'KDD', 'FRED-MD', 'US', 'COVID']
    database_title = " ".join([w.upper() if w.upper() in uppercase_word else w for w in database_title.split(' ')])
    return database_title


def pivot_selected_error_measure_results(selected_error_measure_results):
    """
    Pivots error measure results for visualization.
    
    Args:
        selected_error_measure_results (DataFrame): Data with error measures.
    
    Returns:
        DataFrame: Pivoted data on model and database.
    """    
    selected_error_measure_results = selected_error_measure_results.copy()
    selected_error_measure_results.columns = ['selected_error_measure']
    selected_error_measure_results.reset_index(inplace=True)
    selected_error_measure_results = selected_error_measure_results.rename({'index': 'name'}, axis=1)
    selected_error_measure_results['model'] = selected_error_measure_results['name'].apply(lambda x: get_model_name(x))
    selected_error_measure_results['database'] = selected_error_measure_results['name'].apply(lambda x: get_database_name(x))
    selected_error_measure_results.drop('name', axis=1, inplace=True)
    selected_error_measure_results_pivoted = (
        selected_error_measure_results
        .pivot(index='database', columns='model', values='selected_error_measure')
    )
    return selected_error_measure_results_pivoted


def generate_table2_dataframe(selected_error_measure='Mean MASE', table_name='table2'):
    """
    Generates a DataFrame for a selected error measure and saves it.
    
    Args:
        selected_error_measure (str): The error measure to filter by.
        table_name (str): Name of the output table file.
    
    Returns:
        DataFrame: Pivoted results for the selected error measure.
    """    
    fixed_horizon_errors = os.listdir('results/fixed_horizon_errors')
    fixed_horizon_errors = [
        f for f in fixed_horizon_errors
        if not bool(re.search('smape[.]txt|mae[.]txt|mase[.]txt|msmape[.]txt|rmse[.]txt', f))
    ]
    fixed_horizon_error_results = {}
    for error_analysis in fixed_horizon_errors:
        with open(f'results/fixed_horizon_errors/{error_analysis}', 'r') as f:
            results = f.readlines()
        fixed_horizon_error_results[error_analysis] = results
    fixed_horizon_error_results = {
        f: transform_string_results_to_dict(r) for f, r in fixed_horizon_error_results.items()
    }
    selected_error_measure_results = pd.DataFrame(fixed_horizon_error_results).transpose()[[selected_error_measure]]
    pivoted_results = pivot_selected_error_measure_results(selected_error_measure_results)
    ordered_models = (
        [c for c in ORDER_MODELS if c in list(pivoted_results.columns)]
        + [c for c in list(pivoted_results.columns) if c not in ORDER_MODELS]
    )
    pivoted_results = pivoted_results[ordered_models]
    ordered_databases = (
        [c for c in ORDER_DATASETS if c in list(pivoted_results.index)]
        + [c for c in list(pivoted_results.index) if c not in ORDER_DATASETS]
    )
    pivoted_results = pivoted_results.loc[ordered_databases]
    csv_file_path = os.path.join(BASE_DIR, 'output', 'tables', f'{table_name}.csv')
    results_folder = os.path.join(BASE_DIR, 'output', 'tables')
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    pivoted_results = pivoted_results.reset_index().rename({'database': 'Dataset'}, axis=1)
    pivoted_results.to_csv(csv_file_path, index=False)
    pivoted_results.to_excel(csv_file_path.replace('.csv', '.xlsx'), index=False)
        

if __name__== '__main__':
    generate_table1_dataframe(print_dataset_name=True)
    generate_table2_dataframe()
