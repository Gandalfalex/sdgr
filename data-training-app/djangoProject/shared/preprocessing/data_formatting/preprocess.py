import numpy as np


class PreProcessing:
    data = []
    min_length = 100
    starting_lengths: []

    def __init__(self):
        self.starting_lengths = []

    def get_name(self):
        pass

    def set_data(self, data):
        self.starting_lengths = [len(x) for x in data]
        self.data = data

    def set_config(self, config):
        pass

    def get_smallest_list(self):
        self.starting_lengths = [len(x) for x in self.data]
        print(f"starting_lengths: {self.starting_lengths}")
        return min(self.starting_lengths)


    # TODO what to do here? normalization on each or in total?
    def get_highest_absolut_value(self):
        max_value = 0
        for signal in self.data:
            max_value = max(max_value, max(abs(min(signal)), max(signal)))

        return max_value

    def get_median(self):
        m = [sum(x) for x in self.data]
        return sum(m) / len(m)

    def process(self):
        pass

    def convert_back(self, values):
        pass

    def interpolate_original_length(self):
        reconstructed_data = []
        for x, original_length in zip(self.data, self.starting_lengths):
            reconstructed_x = np.interp(np.linspace(0, len(x) - 1, original_length), np.arange(len(x)), x)
            reconstructed_data.append(reconstructed_x.tolist())
        return reconstructed_data
