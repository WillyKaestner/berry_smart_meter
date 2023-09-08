import pandas as pd
import database as db
import crud


def get_hist_consumption_data() -> pd.DataFrame:
    repository = crud.SqlAlchemyEnergyData(db=db.get_db())
    data = repository.list()
    df_raw = pd.DataFrame([(x.created_at, x.real_power) for x in data],
                          columns=['timestamp_begin', 'consumption_milliwatt'])
    return df_raw


def data_transformation(raw_data: pd.DataFrame) -> pd.DataFrame:
    df = raw_data.copy()
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

    return df_final
