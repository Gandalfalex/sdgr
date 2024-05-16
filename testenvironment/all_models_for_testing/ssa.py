import numpy as np
import pandas as pd

from all_models_for_testing.general_ml_model import GeneralModel

"""
https://www.kaggle.com/code/jdarcy/introducing-ssa-for-time-series-decomposition
"""


class SingularSpectrumAnalysis(GeneralModel):
    window_length = 2

    def prepare_data(self, window_length, save_mem=True):

        self.N = len(self.data)
        if not 2 <= window_length <= self.N / 2:
            raise ValueError("The window length must be in the interval [2, N/2].")

        self.window_length = window_length
        self.orig_TS = pd.Series(self.data)
        self.K = self.N - self.window_length + 1

        # Embed the time series in a trajectory matrix
        self.X = np.array([self.orig_TS.values[i:window_length + i] for i in range(0, self.K)]).T

        # Decompose the trajectory matrix
        self.U, self.Sigma, VT = np.linalg.svd(self.X)
        self.d = np.linalg.matrix_rank(self.X)

        self.ts_data_split = np.zeros((self.N, self.d))

        if not save_mem:
            # Construct and save all the elementary matrices
            self.X_elem = np.array([self.Sigma[i] * np.outer(self.U[:, i], VT[i, :]) for i in range(self.d)])

            # Diagonally average the elementary matrices, store them as columns in array.
            for i in range(self.d):
                X_rev = self.X_elem[i, ::-1]
                self.ts_data_split[:, i] = [X_rev.diagonal(j).mean() for j in
                                            range(-X_rev.shape[0] + 1, X_rev.shape[1])]

            self.V = VT.T
        else:
            # Reconstruct the elementary matrices without storing them
            for i in range(self.d):
                X_elem = self.Sigma[i] * np.outer(self.U[:, i], VT[i, :])
                X_rev = X_elem[::-1]
                self.ts_data_split[:, i] = [X_rev.diagonal(j).mean() for j in
                                            range(-X_rev.shape[0] + 1, X_rev.shape[1])]

            self.X_elem = "Re-run with save_mem=False to retain the elementary matrices."

            # The V array may also be very large under these circumstances, so we won't keep it.
            self.V = "Re-run with save_mem=False to retain the V matrix."

        # Calculate the w-correlation matrix.
        self.calc_wcorr()

    def calc_wcorr(self):
        # Calculate the weights
        w = np.array(
            list(np.arange(self.window_length) + 1) + [self.window_length] * (self.K - self.window_length - 1) + list(
                np.arange(self.window_length) + 1)[::-1])

        def w_inner(F_i, F_j):
            return w.dot(F_i * F_j)

        # Calculated weighted norms, ||F_i||_w, then invert.
        F_wnorms = np.array([w_inner(self.ts_data_split[:, i], self.ts_data_split[:, i]) for i in range(self.d)])
        F_wnorms = F_wnorms ** -0.5

        # Calculate Wcorr.
        self.Wcorr = np.identity(self.d)
        for i in range(self.d):
            for j in range(i + 1, self.d):
                self.Wcorr[i, j] = abs(
                    w_inner(self.ts_data_split[:, i], self.ts_data_split[:, j]) * F_wnorms[i] * F_wnorms[j])
                self.Wcorr[j, i] = self.Wcorr[i, j]

    def sum_up_data(self, depth=0):
        sum_data = np.zeros(self.ts_data_split.shape[0])
        if depth > 0:
            max_depth = min(depth, len(self.ts_data_split[0]))
            for i in range(len(self.ts_data_split)):
                sum_data[i] = sum(self.ts_data_split[i][:max_depth])
        else:
            for i in range(len(self.ts_data_split)):
                sum_data[i] = sum(self.ts_data_split[i])
        return sum_data.tolist()

    def run(self, precision=False):

        if self.run_information.get_all:
            all_information = []
            for data in self.data:
                self.data = np.array(data)
                self.prepare_data(self.run_information.split)
                all_information.append(self.sum_up_data(self.run_information.precision))
            self.run_information.set_prediction(all_information)
            return self.run_information

        self.data = self.data[0]
        self.prepare_data(self.run_information.split)
        self.run_information.set_prediction(self.sum_up_data(self.run_information.precision))
        return self.run_information

    def predict_from_function(self, prediction_length):
        pass
