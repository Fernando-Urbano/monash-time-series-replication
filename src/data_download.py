import requests
import zipfile
import os
from io import BytesIO

import config
from pathlib import Path
from doit.tools import run_once


OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)

URLS = {
    'm1_yearly_dataset.tsf': 'https://zenodo.org/records/4656193/files/m1_yearly_dataset.zip?download=1',
    'm1_quarterly_dataset.tsf': 'https://zenodo.org/records/4656154/files/m1_quarterly_dataset.zip?download=1',
    'm1_monthly_dataset.tsf': 'https://zenodo.org/records/4656159/files/m1_monthly_dataset.zip?download=1',
    'm3_yearly_dataset.tsf': 'https://zenodo.org/records/4656222/files/m3_yearly_dataset.zip?download=1',
    'm3_quarterly_dataset.tsf': 'https://zenodo.org/records/4656262/files/m3_quarterly_dataset.zip?download=1',
    'm3_monthly_dataset.tsf': 'https://zenodo.org/records/4656298/files/m3_monthly_dataset.zip?download=1',
    'm3_other_dataset.tsf': 'https://zenodo.org/records/4656335/files/m3_other_dataset.zip?download=1',
    'm4_yearly_dataset.tsf': 'https://zenodo.org/records/4656379/files/m4_yearly_dataset.zip?download=1',
    'm4_weekly_dataset.tsf': 'https://zenodo.org/records/4656522/files/m4_weekly_dataset.zip?download=1',
    'm4_quarterly_dataset.tsf': 'https://zenodo.org/records/4656410/files/m4_quarterly_dataset.zip?download=1',
    'm4_monthly_dataset.tsf': 'https://zenodo.org/records/4656480/files/m4_monthly_dataset.zip?download=1',
    'm4_daily_dataset.tsf': 'https://zenodo.org/records/4656548/files/m4_daily_dataset.zip?download=1',
    'm4_hourly_dataset.tsf': 'https://zenodo.org/records/4656589/files/m4_hourly_dataset.zip?download=1',
    'tourism_monthly_dataset.tsf': 'https://zenodo.org/records/4656096/files/tourism_monthly_dataset.zip?download=1',
    'tourism_quarterly_dataset.tsf': 'https://zenodo.org/records/4656093/files/tourism_quarterly_dataset.zip?download=1',
    'tourism_yearly_dataset.tsf': 'https://zenodo.org/records/4656103/files/tourism_yearly_dataset.zip?download=1',
    'cif_2016_dataset.tsf': 'https://zenodo.org/records/4656042/files/cif_2016_dataset.zip?download=1',
    'london_smart_meters_dataset_without_missing_values.tsf': 'https://zenodo.org/records/4656091/files/london_smart_meters_dataset_without_missing_values.zip?download=1',
    'london_smart_meters_dataset_with_missing_values.tsf': 'https://zenodo.org/records/4656072/files/london_smart_meters_dataset_with_missing_values.zip?download=1',
    'australian_electricity_demand_dataset.tsf': 'https://zenodo.org/records/4659727/files/australian_electricity_demand_dataset.zip?download=1',
    'wind_farms_minutely_dataset_with_missing_values.tsf': 'https://zenodo.org/records/4654909/files/wind_farms_minutely_dataset_with_missing_values.zip?download=1',
    'wind_farms_minutely_dataset_without_missing_values.tsf': 'https://zenodo.org/records/4654858/files/wind_farms_minutely_dataset_without_missing_values.zip?download=1',
    'dominick_dataset.tsf': 'https://zenodo.org/records/4654802/files/dominick_dataset.zip?download=1',
    'bitcoin_dataset_without_missing_values.tsf': 'https://zenodo.org/records/5122101/files/bitcoin_dataset_without_missing_values.zip?download=1',
    'bitcoin_dataset_with_missing_values.tsf': 'https://zenodo.org/records/5121965/files/bitcoin_dataset_with_missing_values.zip?download=1',
    'pedestrian_counts_dataset.tsf': 'https://zenodo.org/records/4656626/files/pedestrian_counts_dataset.zip?download=1',
    'vehicle_trips_dataset_with_missing_values.tsf': 'https://zenodo.org/records/5122535/files/vehicle_trips_dataset_with_missing_values.zip?download=1',
    'vehicle_trips_dataset_without_missing_values.tsf': 'https://zenodo.org/records/5122537/files/vehicle_trips_dataset_without_missing_values.zip?download=1',
    'kdd_cup_2018_dataset_with_missing_values.tsf': 'https://zenodo.org/records/4656719/files/kdd_cup_2018_dataset_with_missing_values.zip?download=1',
    'kdd_cup_2018_dataset_without_missing_values.tsf': 'https://zenodo.org/records/4656756/files/kdd_cup_2018_dataset_without_missing_values.zip?download=1',
    'weather_dataset.tsf': 'https://zenodo.org/records/4654822/files/weather_dataset.zip?download=1',
    'nn5_daily_dataset_with_missing_values.tsf': 'https://zenodo.org/records/4656110/files/nn5_daily_dataset_with_missing_values.zip?download=1',
    'nn5_daily_dataset_without_missing_values.tsf': 'https://zenodo.org/records/4656117/files/nn5_daily_dataset_without_missing_values.zip?download=1',
    'nn5_weekly_dataset.tsf': 'https://zenodo.org/records/4656125/files/nn5_weekly_dataset.zip?download=1',
    'kaggle_web_traffic_dataset_with_missing_values.tsf': 'https://zenodo.org/records/4656080/files/kaggle_web_traffic_dataset_with_missing_values.zip?download=1',
    'kaggle_web_traffic_dataset_without_missing_values.tsf': 'https://zenodo.org/records/4656075/files/kaggle_web_traffic_dataset_without_missing_values.zip?download=1',
    'kaggle_web_traffic_weekly_dataset.tsf': 'https://zenodo.org/records/4656664/files/kaggle_web_traffic_weekly_dataset.zip?download=1',
    'solar_10_minutes_dataset.tsf': 'https://zenodo.org/records/4656144/files/solar_10_minutes_dataset.zip?download=1',
    'solar_weekly_dataset.tsf': 'https://zenodo.org/records/4656151/files/solar_weekly_dataset.zip?download=1',
    'electricity_hourly_dataset.tsf': 'https://zenodo.org/records/4656140/files/electricity_hourly_dataset.zip?download=1',
    'electricity_weekly_dataset.tsf': 'https://zenodo.org/records/4656141/files/electricity_weekly_dataset.zip?download=1',
    'car_parts_dataset_with_missing_values.tsf': 'https://zenodo.org/records/4656022/files/car_parts_dataset_with_missing_values.zip?download=1',
    'car_parts_dataset_without_missing_values.tsf': 'https://zenodo.org/records/4656021/files/car_parts_dataset_without_missing_values.zip?download=1',
    'fred_md_dataset.tsf': 'https://zenodo.org/records/4654833/files/fred_md_dataset.zip?download=1',
    'traffic_hourly_dataset.tsf': 'https://zenodo.org/records/4656132/files/traffic_hourly_dataset.zip?download=1',
    'traffic_weekly_dataset.tsf': 'https://zenodo.org/records/4656135/files/traffic_weekly_dataset.zip?download=1',
    'rideshare_dataset_with_missing_values.tsf': 'https://zenodo.org/records/5122114/files/rideshare_dataset_with_missing_values.zip?download=1',
    'rideshare_dataset_without_missing_values.tsf': 'https://zenodo.org/records/5122232/files/rideshare_dataset_without_missing_values.zip?download=1',
    'hospital_dataset.tsf': 'https://zenodo.org/records/4656014/files/hospital_dataset.zip?download=1',
    'covid_deaths_dataset.tsf': 'https://zenodo.org/records/4656009/files/covid_deaths_dataset.zip?download=1',
    'temperature_rain_dataset_with_missing_values.tsf': 'https://zenodo.org/records/5129073/files/temperature_rain_dataset_with_missing_values.zip?download=1',
    'temperature_rain_dataset_without_missing_values.tsf': 'https://zenodo.org/records/5129091/files/temperature_rain_dataset_without_missing_values.zip?download=1',
    'sunspot_dataset_with_missing_values.tsf': 'https://zenodo.org/records/4654773/files/sunspot_dataset_with_missing_values.zip?download=1',
    'sunspot_dataset_without_missing_values.tsf': 'https://zenodo.org/records/4654722/files/sunspot_dataset_without_missing_values.zip?download=1',
    'saugeenday_dataset.tsf': 'https://zenodo.org/records/4656058/files/saugeenday_dataset.zip?download=1',
    'us_births_dataset.tsf': 'https://zenodo.org/records/4656049/files/us_births_dataset.zip?download=1',
    'solar_4_seconds_dataset.tsf': 'https://zenodo.org/records/4656027/files/solar_4_seconds_dataset.zip?download=1',
    'wind_4_seconds_dataset.tsf': 'https://zenodo.org/records/4656032/files/wind_4_seconds_dataset.zip?download=1',
}


def download_and_extract_zip(url, destination_dir):
    # Send a GET request to the URL
    response = requests.get(url)
    # Raise an exception for bad status codes
    response.raise_for_status()
    
    # Extract the content of the zip file into memory
    with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
        # List the contents of the zip file
        file_list = zip_file.namelist()
        # Extract the first file from the zip file (you can modify this as needed)
        first_file_name = file_list[0]
        # Extract the file to a temporary directory
        zip_file.extract(first_file_name, destination_dir)
    
    # Construct the path to the extracted file
    extracted_file_path = os.path.join(destination_dir, first_file_name)
    
    return extracted_file_path
    


# if __name__ == '__main__':
#     # Example usage
#     for key, url_v in URLS.items():
#         # url = "https://zenodo.org/records/4656080/files/kaggle_web_traffic_dataset_with_missing_values.zip?download=1"
#         print('---')
#         print('Starting the download for {}'.format(key))
#         url = url_v
#         os.makedirs(DATA_DIR, exist_ok=True)
#         extracted_file_path = download_and_extract_zip(url, DATA_DIR)
#         print('Done')
#         print('---\n')