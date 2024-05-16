import numpy as np
from scipy.optimize import curve_fit


class IMFReconstructor:
    def __init__(self):
        self.fitted_functions = []
        self.params = []

    @staticmethod
    def sinusoidal(x, A, omega, phi, c):
        return A * np.sin(omega * x + phi) + c

    def fit_imfs(self, imfs, x):
        """
        Fit a sinusoidal function to each IMF and store the fitted functions.

        :param imfs: A 2D numpy array where each row represents an IMF.
        :param x: The x values corresponding to the IMFs.
        """

        self.fitted_functions = []
        self.params = []
        try:
            for imf in imfs:
                initial_guess = [np.std(imf), 2 * np.pi / (x[-1] - x[0]), 0, np.mean(imf)]

                params, _ = curve_fit(self.sinusoidal, x, imf, p0=initial_guess)
                self.params.append(params)
                self.fitted_functions.append(lambda x, params=params: self.sinusoidal(x, *params))
        except Exception as e:
            print(e)

    def reconstruct(self, x):
        """
        Evaluate the sum of the fitted functions at the given x values.

        :param x: The x values at which to evaluate the sum of the fitted functions.
        :return: The reconstructed time series.
        """
        return sum(f(x) for f in self.fitted_functions)
