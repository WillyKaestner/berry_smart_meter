from forecast import forecast_prophet, consumption_data


# Select forecast strategy
FORECAST_STRATEGY = forecast_prophet.ProphetForecast()

# Forecast model generation and prediction
data_raw = consumption_data.get_hist_consumption_data()
data_transformed = consumption_data.data_transformation(data_raw)
forecast_data = FORECAST_STRATEGY.generate_forecast(data_transformed)
