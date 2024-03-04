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


def generate_table1_dataframe(DATA_DIR):

    # Get a list of all files in the data directory
    all_files = os.listdir(DATA_DIR)
    
    # Filter files with the '.tsf' extension using list comprehension
    files_with_extension = [file for file in all_files if file.endswith('.tsf')]

    df_table1 = pd.DataFrame(columns=['Dataset','# of Series','Frequency','Forecast_horizon','Missing_values','Equal_length','Min_Length','Max_Length','Competition'])
    df_table1['Missing_values'] = df_table1['Missing_values'].astype(bool)
    df_table1['Equal_length'] = df_table1['Equal_length'].astype(bool)
    df_table1['Competition'] = df_table1['Competition'].astype(bool)
    # Example of usage
    for f1 in files_with_extension:
        loaded_data, frequency, forecast_horizon, contain_missing_values, contain_equal_length, competition_dataset = convert_tsf_to_dataframe(str(DATA_DIR) + '/' + f1)
        loaded_data['len_series'] = loaded_data['series_value'].apply(lambda x: len(x))
        df_append = pd.DataFrame([{'Dataset':f1.split('.')[0], '# of Series':loaded_data.shape[0],'Frequency':frequency,'Forecast_horizon':forecast_horizon,'Missing_values':contain_missing_values,'Equal_length':contain_equal_length,'Min_Length':loaded_data['len_series'].min(),'Max_Length':loaded_data['len_series'].max(),'Competition':competition_dataset}])
        df_append = pd.DataFrame([{'Dataset':f1.split('.')[0], '# of Series':loaded_data.shape[0],'Frequency':frequency,'Forecast_horizon':forecast_horizon,'Missing_values':contain_missing_values,'Equal_length':contain_equal_length,'Min_Length':loaded_data['len_series'].min(),'Max_Length':loaded_data['len_series'].max(),'Competition':competition_dataset}])
        
        df_table1 = pd.concat([df_table1,df_append], axis=0)

    # Define the path to the CSV file
    csv_file_path = os.path.join(BASE_DIR, 'results', 'Table1.csv')

    # Create the results folder if it doesn't exist
    results_folder = os.path.join(BASE_DIR, 'results')
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
        
    df_table1.to_csv(csv_file_path)
    return df_table1

# if __name__=='__main__':
#     print(generate_table1_dataframe(DATA_DIR=DATA_DIR))