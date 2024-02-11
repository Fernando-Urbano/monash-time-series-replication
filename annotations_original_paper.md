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

# Data
`utils/data_loader.R`: Data is loaded in to R environment in tsibble format and can be loaded into Pandas dataframe using the same file.

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




