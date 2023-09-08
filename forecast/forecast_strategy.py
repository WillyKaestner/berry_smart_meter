from abc import ABC, abstractmethod
import pandas as pd


class ForecastStrategy(ABC):
    @abstractmethod
    def generate_forecast(self, base_data: pd.DataFrame) -> pd.DataFrame:
        """Calculate forecast data based on historical base data"""
