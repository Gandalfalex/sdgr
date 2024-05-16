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


    def get_smallest_list(self):
        self.starting_lengths = [len(x) for x in self.data]
        return min(self.starting_lengths)


    def get_highest_absolut_value(self):
        max_value = 0
        for signal in self.data:
            max_value = max(max_value, max(abs(min(signal)), max(signal)))

        return max_value

    def get_median(self):
        m = [sum(x) for x in self.data]
        return sum(m) / len(m)

    def process(self):
        min_len = self.get_smallest_list() if self.min_length == 0 or self.min_length is None else self.min_length
        self.max_red = self.get_highest_absolut_value()
        print(self.max_red)
        self.data = [np.interp(np.linspace(0, len(x) - 1, min_len), np.arange(len(x)), x).tolist() for x in
                     self.data]
        self.max_red = self.max_red * 2
        # self.data = [x[:min_length] for x in self.data]
        self.data = [np.array([0.5 + (i / self.max_red) for i in d]) for d in self.data]
        return self.data, {"max_red": self.max_red, "min_len": min_len}

    def convert_back(self, values):
        pass

    def interpolate_original_length(self):
        reconstructed_data = []
        for x, original_length in zip(self.data, self.starting_lengths):
            reconstructed_x = np.interp(np.linspace(0, len(x) - 1, original_length), np.arange(len(x)), x)
            reconstructed_data.append(reconstructed_x.tolist())
        return reconstructed_data
