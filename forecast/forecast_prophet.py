import pandas as pd
from prophet import Prophet
from .forecast_strategy import ForecastStrategy


class ProphetForecast(ForecastStrategy):

    def __init__(self, periods: int = 24, freq: str = "0.25H"):
        self.periods = periods
        self.freq = freq

    def generate_forecast(self, base_data: pd.DataFrame) -> pd.DataFrame:
        # Convert Dataframe for Prophet
        df_base = base_data.rename({"timestamp_begin": "ds", "consumption_watt": "y"}, axis='columns')
        df_base["ds"] = df_base["ds"].dt.tz_localize(None)

        # Fit model
        m = Prophet()
        m.fit(df_base)

        # Prediction horizon
        future = m.make_future_dataframe(periods=self.periods, freq=self.freq)
        future.tail()
        print(future.tail())

        # Predict
        forecast = m.predict(future)

        print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(35))
        return forecast
