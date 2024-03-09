from datetime import datetime
from distutils.util import strtobool

import pandas as pd
import os
import config
from pathlib import Path

BASE_DIR = Path(config.BASE_DIR)
OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)

'''
This file is taken from https://github.com/rakshitha123/TSForecasting
Converts the contents in a .tsf file into a dataframe and returns it along with other meta-data of the dataset: 
frequency, horizon, whether the dataset contains missing values and whether the series have equal lengths

Parameters
full_file_path_and_name - complete .tsf file path
replace_missing_vals_with - a term to indicate the missing values in series in the returning dataframe
value_column_name - Any name that is preferred to have as the name of the column containing series values in the returning dataframe
'''

def convert_tsf_to_dataframe(
    full_file_path_and_name,
    replace_missing_vals_with="NaN",
    value_column_name="series_value",
):
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
        ]
    },
    'M3': {
        'Domain': 'Multiple',
        'Datasets': [
            'm3_monthly_dataset.tsf',
            'm3_quarterly_dataset.tsf',
            'm3_yearly_dataset.tsf',
            'm3_other_dataset.tsf'
        ]
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
        ]
    },
    'Tourism': {
        'Domain': 'Tourism',
        'Datasets': [
            'tourism_monthly_dataset.tsf',
            'tourism_quarterly_dataset.tsf',
            'tourism_yearly_dataset.tsf'
        ]
    },
    'CIF 2016': {
        'Domain': 'Banking',
        'Datasets': [
            'cif_2016_dataset.tsf'
        ]
    },
    'London Smart Meters': {
        'Domain': 'Energy',
        'Datasets': [
            'london_smart_meters_dataset_with_missing_values.tsf',
        ]
    },
    'Aus. Electricity Demand': {
        'Domain': 'Energy',
        'Datasets': [
            'australian_electricity_demand_dataset.tsf'
        ]
    },
    'Wind Farms': {
        'Domain': 'Energy',
        'Datasets': [
            'wind_farms_minutely_dataset_with_missing_values.tsf',
        ]
    },
    'Dominick': {
        'Domain': 'Sales',
        'Datasets': [
            'dominick_dataset.tsf'
        ]
    },
    'Bitcoin': {
        'Domain': 'Economic',
        'Datasets': [
            'bitcoin_dataset_with_missing_values.tsf'
        ]
    },
    'Pedestrian Counts': {
        'Domain': 'Transport',
        'Datasets': [
            'pedestrian_counts_dataset.tsf'
        ]
    },
    'Vehicle Trips': {
        'Domain': 'Transport',
        'Datasets': [
            'vehicle_trips_dataset_with_missing_values.tsf'
        ]
    },
    'KDD Cup 2018': {
        'Domain': 'Transport',
        'Datasets': [
            'kdd_cup_2018_dataset_with_missing_values.tsf'
        ]
    },
    'Weather': {
        'Domain': 'Weather',
        'Datasets': [
            'weather_dataset.tsf'
        ]
    },
    'NN5': {
        'Domain': 'Banking',
        'Datasets': [
            'nn5_daily_dataset_with_missing_values.tsf',
            'nn5_weekly_dataset.tsf'
        ]
    },
    'Kaggle Web Traffic': {
        'Domain': 'Web Traffic',
        'Datasets': [
            'kaggle_web_traffic_dataset_with_missing_values.tsf'
        ]
    },
    'Solar': {
        'Domain': 'Energy',
        'Datasets': [
            'solar_10_minutes_dataset.tsf',
            'solar_weekly_dataset.tsf'
        ]
    },
    'Electricity': {
        'Domain': 'Energy',
        'Datasets': [
            'electricity_hourly_dataset.tsf',
            'electricity_weekly_dataset.tsf'
        ]
    },
    'Car Parts': {
        'Domain': 'Sales',
        'Datasets': [
            'car_parts_dataset_with_missing_values.tsf'
        ]
    },
    'FRED-MD': {
        'Domain': 'Economics',
        'Datasets': [
            'fred_md_dataset.tsf'
        ]
    },
    'San Francisco Traffic': {
        'Domain': 'Transport',
        'Datasets': [
            'traffic_hourly_dataset.tsf',
            'traffic_weekly_dataset.tsf'
        ]
    },
    'Rideshare': {
        'Domain': 'Transport',
        'Datasets': [
            'rideshare_dataset_with_missing_values.tsf'
        ]
    },
    'Hospital': {
        'Domain': 'Health',
        'Datasets': [
            'hospital_dataset.tsf'
        ]
    },
    'COVID Deaths': {
        'Domain': 'Nature',
        'Datasets': [
            'covid_deaths_dataset.tsf'
        ]
    },
    'Temperature Rain': {
        'Domain': 'Nature',
        'Datasets': [
            'temperature_rain_dataset_with_missing_values.tsf'
        ]
    },
    'Sunspot': {
        'Domain': 'Nature',
        'Datasets': [
            'sunspot_dataset_with_missing_values.tsf'
        ]
    },
    'Saugeen River Flow': {
        'Domain': 'Nature',
        'Datasets': [
            'saugeenday_dataset.tsf'
        ]
    },
    'US Births': {
        'Domain': 'Nature',
        'Datasets': [
            'us_births_dataset.tsf'
        ]
    },
    'Solar Power': {
        'Domain': 'Energy',
        'Datasets': [
            'solar_weekly_dataset.tsf'
        ]
    },
    'Wind Power': {
        'Domain': 'Energy',
        'Datasets': [
            'wind_4_seconds_dataset.tsf'
        ]
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
        'Multivariate': False if 'Multivariate' not in list(dataset_information.keys()) else True
    }
    for dataset in dataset_information['Datasets']:
        loaded_data, frequency, forecast_horizon, contain_missing_values, contain_equal_length, competition_dataset = convert_tsf_to_dataframe(str(DATA_DIR) + '/' + dataset)
        loaded_data['len_series'] = loaded_data['series_value'].apply(lambda x: len(x))
        min_len = loaded_data['len_series'].min()
        max_len = loaded_data['len_series'].max()
        dataset_statistics['Min. Length'] = min_len if min_len < dataset_statistics['Min. Length'] else dataset_statistics['Min. Length']
        dataset_statistics['Max. Length'] = max_len if max_len > dataset_statistics['Max. Length'] else dataset_statistics['Max. Length']
        dataset_statistics['No: of Series'] += loaded_data.shape[0]
        if dataset_statistics['Missing'] is None:
            dataset_statistics['Missing'] = contain_missing_values
        if dataset_statistics['Competition'] is None:
            dataset_statistics['Competition'] = competition_dataset
    return dataset_statistics


def generate_table1_dataframe():
    datasets_statistics = {}
    for dataset_name, dataset_info in DATASETS_TO_INFO.items():
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
    return True


if __name__== '__main__':
    generate_table1_dataframe()