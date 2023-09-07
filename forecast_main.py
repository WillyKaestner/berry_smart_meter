import pandas as pd
from prophet import Prophet
import database as db
import crud

#%% Fetch consumption data
repository = crud.SqlAlchemyEnergyData(db=db.get_db())
data = repository.list()
df_raw = pd.DataFrame([(x.created_at, x.real_power) for x in data],
                      columns=['timestamp_begin', 'consumption_milliwatt'])
#%%
# Data conversion
df = df_raw.copy()
df["consumption_watt"] = df["consumption_milliwatt"] / 100
df.drop(columns=["consumption_milliwatt"], inplace=True)

# Sort by timestamp
df.set_index("timestamp_begin", inplace=True)
df_sorted = df.sort_index()

# Data Selection
start = pd.Timestamp(year=2023, month=7, day=30, tz="UTC")
end = pd.Timestamp(year=2023, month=9, day=5, tz="UTC")
df_selection = df_sorted[start:end]

# Turn negative value to positive
df_positive = df_selection["consumption_watt"].abs()

# Final Dataframe
df_final = df_positive.reset_index()

# Plotting
# pd.options.plotting.backend = "plotly"
# fig = df_selection.plot()
# fig.show()

#%%
# Convert Dataframe for Prophet
df_base = df_final.rename({"timestamp_begin": "ds", "consumption_watt": "y"}, axis='columns')
df_base["ds"] = df_base["ds"].dt.tz_localize(None)

# Fit model
m = Prophet()
m.fit(df_base)

# Prediction horizon
future = m.make_future_dataframe(periods=24, freq='0.25H')
future.tail()
print(future.tail())

# Predict
forecast = m.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(35))
