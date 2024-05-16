import numpy as np

from shared.preprocessing.data_formatting.preprocess import PreProcessing


class LinearTrendProcessing(PreProcessing):
    """
    saving the correct detrended version is currently only considered for one element.
    optional TODO, extend later
    """
    a = None
    b = None
    t = None

    def set_config(self, config):
        self.a = config.get("a")
        self.b = config.get("b")
        # self.t = config.get("t")

    def process(self):
        self.t = np.arange(len(self.data[0]))
        min_len = self.get_smallest_list() if self.min_length == 0 or self.min_length is None else self.min_length
        if self.a is None or self.b is None or self.t is None:
            self.t = np.arange(len(self.data[0]))
            coefficients = np.polyfit(self.t, self.data[0], 1)
            self.a, self.b = coefficients

        detrend = np.zeros(min_len)
        for _ in self.data:
            y_trend = np.float64(self.a) * self.t + np.float64(self.b)
            detrend = self.data - y_trend

        self.data = [np.interp(np.linspace(0, len(x) - 1, min_len), np.arange(len(x)), x).tolist() for x in detrend]
        return self.data, {"a": self.a, "b": self.b, "t": self.t, "min_len": min_len}

    def convert_back(self, values):
        a = values.get("a")
        b = values.get("b")
        t = values.get("t")
        self.data = self.data + (a * t + b)
        return self.interpolate_original_length()

    def get_name(self):
        return "LinearTrendRemove"
