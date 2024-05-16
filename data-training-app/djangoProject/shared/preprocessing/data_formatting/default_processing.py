import numpy as np

from shared.preprocessing.data_formatting.preprocess import PreProcessing


class DefaultPreprocessing(PreProcessing):

    def set_config(self, config):
        pass

    def process(self):
        min_len = self.get_smallest_list() if self.min_length == 0 or self.min_length is None else self.min_length
        self.data = [np.interp(np.linspace(0, len(x) - 1, min_len), np.arange(len(x)), x).tolist() for x in
                     self.data]
        return self.data, {"min_len": min_len}

    def convert_back(self, values):
        return self.interpolate_original_length()

    def get_name(self):
        return "DefaultProcessing"
