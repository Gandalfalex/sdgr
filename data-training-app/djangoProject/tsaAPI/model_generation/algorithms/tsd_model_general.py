import numpy as np

from tsaAPI.model_generation.run_information import RunInformation


class GeneralTSDModel:
    data = None
    x_values = None
    run_information: RunInformation = None

    def run(self, precision=False):
        pass

    def set_config(self, config: RunInformation):
        self.run_information = config

    def set_data(self, data):
        self.data = data

    def set_x_values(self, data):
        self.x_values = data

    def remove_linear_trend(self, data):
        t = np.arange(len(data))
        if t == 0:
            return data, (0, 0, 0)
        coefficients = np.polyfit(t, data, 1)
        a, b = coefficients
        y_trend = a * t + b
        y_detrended = data - y_trend
        return y_detrended, (a, b, t)

    def add_linear_trend(self, data, coefficients):
        a, b, t = coefficients
        return data + (a * t + b)

    def sum_up_data(self):
        pass

    def create_returnable_data(self, data, precision):
        values = []
        for m in range(0, len(data[0])):
            if precision:
                min_len = [data[i][m] for i in range(len(data))]
            else:
                min_len = [round(data[i][m], 4) for i in range(len(data))]
            values.append({"level": m, "data": min_len})
        return values

    def predict_from_function(self, prediction_length):
        pass

    def __init__(self):
        self.data = None

