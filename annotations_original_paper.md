# Software Packages Used
| Software/Package       | Version        | 
|------------------------|:--------------:|
| R                      |  4.0.2         |
| Python                 |  3.7.4         |
| forecast               |  8.12          |
| glmnet                 |  4.0.2         |
| catboost               |  0.24.1        |
| smooth                 |  2.6.0         |
| GluonTS                |  0.8.0         |

# How can we create a virtual environment?
Conda allows us to create a virtul environment specifying the versions of python and R:

```bash
conda create -n finm python=3.12 r-base=4.1.0
```

Afterwards, we can run for Python:

```bash
pip install -r requirements.tx
```

And we create the following for R:

```R
# install_packages.R

# List of required packages
packages <- c("dplyr", "ggplot2", "tidyr", "readr")

# Function to install missing packages
install_if_missing <- function(packages) {
  new_packages <- packages[!(packages %in% installed.packages()[,"Package"])]
  if(length(new_packages)) install.packages(new_packages)
}

# Install the packages
install_if_missing(packages)
```

The script runs with the following commands:

```
Rscript install_packages.R
```

# Data
`utils/data_loader.R`: Data is loaded in to R environment in tsibble format and can be loaded into Pandas dataframe using the same file.

## data_loader.R
Needs to have `tsibble` installed. Creates function to take the data and convert into a "dataframe format". Supposelly, the data_loader.py does the same for Python and return multiple variables:

```
return (
    loaded_data,
    frequency,
    forecast_horizon,
    contain_missing_values,
    contain_equal_length,
)
```

In it, there is specification about the frequency of the data, horizon forecast and if the dataframe contains missing data.

# Models
- ETS, ARIMA, Theta, TBATS, SES and DHR-ARIMA
- Pooled Regression Model
- CatBoost
- Feed-forward Neural Network and 4 Deeplearning models (DeepAR, N-BEATS, WaveNet and Transformer)
- Feature calculations of all series
- Calculations of 5 error measures to evaluate forecasts

The models are run in the `experiment` folder inside the project.

## Fixed Horizon
The fixed horizon is implemented using `fixed_horizon.R` and `deep_learning_experiments.py`.

## Rolling Origin Forecasting
Rolling horizon forecast is also implemented inside the `experiment` folder. Probably differ from the fixed horizon implementation due changes of the first point of the training data.

## Results 
The results are all stored inside a folder that is generated.

## local_univariate_model.R
Supposely, it is called like that because it makes forecast of a single series independently.

The functions used are all in the same format:

```
get_ets_forecasts <- function(time_series, forecast_horizon){
  tryCatch(
    forecast(forecast:::ets(time_series), h = forecast_horizon)$mean
  ,error = function(e) {
    warning(e)
    get_snaive_forecasts(time_series, forecast_horizon)
  })
}
```

The model is tried and if it does not work a seasonal naive forecast is used. Some models have more steps, for instance, the ARIMA is tried with lambda 0 and, if it does not work, it is tried without specifying lambda. If it is still does not work it is tried without seasonality and, finally, if it still does not work, a naive forecast is used in the same way the ETS did.

## feature_functions.R
Has the function `calculate_features`:

```R
calculate_features <- function(dataset_name, input_file_name, key = NULL, index = NULL, feature_type = "tsfeatures"){
  
  ...

}
```

The function connverts the data of the input file specified as a parameter in loaded data:

```R
loaded_data <- convert_tsf_to_tsibble(file.path(BASE_DIR, "tsf_data", input_file_name, fsep = "/"), VALUE_COL_NAME, key, index)
dataset <- loaded_data[[1]]
frequency <- loaded_data[[2]]
```

The loaded data has the dataset and the frequency. 

If no frequency is specified, the seasonality is automatically 1:

```R
if(!is.null(frequency))
    seasonality <- SEASONALITY_MAP[[frequency]]
  else
    seasonality <- 1
```

Inside the dataset, every series is used individually and converted into a `forecast:::msts`.

The `forecast:::msts` is a Multi-Seasonal Time Series created by Rob Hyndman (coauthor of the project).

For each series in the dataset:

```R
for(s in seq_along(all_serie_names)){
    series_data <- dataset[dataset$series_name == as.character(all_serie_names[s]), ]

    if(is.null(index))
    series <- forecast:::msts(series_data[[VALUE_COL_NAME]], seasonal.periods = seasonality)
    else{
    start_date <- start(as.ts(series_data[, c(index, VALUE_COL_NAME)], frequency = max(seasonality)))

    if(length(start_date) == 1){ # Prepararing the start date according to the format required by stl_features such as peak and trough
    start_date <- c(floor(start_date), floor((start_date - floor(start_date)) * max(seasonality)))
    }

    series <- forecast:::msts(series_data[[VALUE_COL_NAME]], start = start_date, seasonal.periods = seasonality, ts.frequency = floor(max(seasonality)))
    }

    tslist[[s]] <- series
}
```

After, the function loops over the `tslist`:

```
for(i in 1:length(tslist)){
    print(i)
    
    features <- NULL
```

Here, there are three paths:

`tsfeatures`: If the feature_type is `tsfeatures`, the code block calculates a set of time series features using the `tsfeatures` package. It iterates over a predefined list of feature names (`TSFEATURE_NAMES`) and calculates each feature for the current time series. This involves handling missing values and, if necessary, adjusting parameters for certain features to ensure they can be calculated correctly. Additionally, it attempts to calculate seasonal features using stl_features with error handling to manage cases where the default calculation fails.

`catch22`: If the feature_type is "catch22", it calculates the catch22 features for the current time series. Catch22 is a set of 22 features designed to summarize various aspects of time series data.

`lambda`: If the feature_type is "lambda", the code calculates the Box-Cox transformation lambda value for the current time series. The Box-Cox transformation is a way to stabilize the variance across a time series.

After the calculation is done, the results are stored inside the matrix `all_features`:

```
all_features[i,] <- as.numeric(features)
```

This matrix is then written to a CSV file, with the directory and file names determined by the `dataset_name`, `feature_type`, and a base directory `BASE_DIR`. Directories are created as needed using dir.create.

# Integrate a Model
If you want to integrate a model, add a function with the model to the `models/local_univariate_models.R`. The function must be called `get_{name of model}_forecasts`.

```
get_alpha_forecasts <- function(time_series, forecast_horizon){
  # Write the function body here to return the forecasts
}
```

After the function is written, we need to specify it in the `fixed_horizon.R` experiment:

```
do_fixed_horizon_local_forecasting("nn5_daily", "alpha", "nn5_daily_dataset_without_missing_values.tsf", "series_name", "start_timestamp")
```

The `nn5_daily_dataset_without_missing_values` is the dataset where the experiment will be executed.




