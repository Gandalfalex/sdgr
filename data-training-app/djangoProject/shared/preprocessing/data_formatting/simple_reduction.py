import numpy as np

from shared.preprocessing.data_formatting.preprocess import PreProcessing


class SimpleReductionPreprocessing(PreProcessing):
    max_red = None

    def set_config(self, config):
        print(config)
        self.max_red = config.get("max_red")

    def process(self):
        min_len = self.get_smallest_list() if self.min_length == 0 or self.min_length is None else self.min_length
        self.max_red = self.get_highest_absolut_value() if self.max_red is None else self.max_red
        self.data = [np.interp(np.linspace(0, len(x) - 1, min_len), np.arange(len(x)), x).tolist() for x in
                     self.data]
        self.max_red = self.max_red * 2
        # self.data = [x[:min_length] for x in self.data]
        self.data = [[0.5 + (i / self.max_red) for i in d] for d in self.data]
        return self.data, {"max_red": self.max_red, "min_len": min_len}

    def convert_back(self, values):
        max_red = values.get("max_red")
        self.data = [[(i - 0.5) * max_red for i in d] for d in self.data]

        return self.interpolate_original_length()

    def get_name(self):
        return "SimpleReduction"
