from typing import List

import numpy as np

from all_models_for_testing.run_information import RunInformation
from reconstruction.FFTReconstructor import FFTReconstructor
from reconstruction.Reconstructor import IMFReconstructor


class GeneralModel:
    data: List[np.ndarray] = None
    run_information: RunInformation = None

    def set_config(self, config: RunInformation):
        self.run_information = config

    def set_data(self, data: List[np.ndarray]):
        """Set the data attribute of the object.

        :param data: The data to be set.
        :return: None
        """
        self.data = data

    def run(self):
        """
        start running the training
        :param uuid: uuid represents the name,
        :param ml_solution_id: solution id of the configuration
        :return: self.run_information
        """
        pass

    def predict_data_from_model(self):
        """
        get a prediction or rework of the data
        :param data:
        :return:
        """
        pass

    def forcast(self, limit: int, starting_point: int = -1) -> []:
        pass

    def create_image(self, real: List[np.array], synthetic: List[np.array], title: str):
        pass

    def remove_linear_trend(self, data):
        t = np.arange(len(data))
        if t == 0:
            return data, (0, 0, 0)
        coefficients = np.polyfit(t, data, 1)
        a, b = coefficients
        y_trend = a * t + b
        y_detrended = data - y_trend
        print((a, b, t))
        return y_detrended, (a, b, t)

    def add_linear_trend(self, data, coefficients):
        a, b, t = coefficients
        return data + (a * t + b)

    def sum_data(self):
        x = np.array(self.data)
        summed_version = np.zeros(self.data[0].shape)
        for i in x:
            summed_version = summed_version + i
        summed_version = summed_version / len(self.data)
        return summed_version

    def reconstruct(self, imfs):
        reconstructor = FFTReconstructor()
        x = self.data[0]
        test = reconstructor.reconstruct(imfs, x)

        reconstructor = IMFReconstructor()
        reconstructor.fit_imfs(imfs, x)

        # Extend the time points for forecasting
        forecast_time_points = np.arange(len(x) + 100)

        # Forecast the next 100 steps
        forecasted_values = reconstructor.reconstruct(forecast_time_points)
        print(forecasted_values)
