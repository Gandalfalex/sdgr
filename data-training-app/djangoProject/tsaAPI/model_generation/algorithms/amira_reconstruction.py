import numpy as np
import statsmodels.api as sm

from tsaAPI.model_generation.algorithms.tsd_model_general import GeneralTSDModel


class AmiraModel(GeneralTSDModel):

    def run(self, precision=False):
        elements = np.zeros(len(self.data[0]))
        for i in self.data:
            arima_model = sm.tsa.arima.ARIMA(i, order=(1, 1, 1))
            arima_results = arima_model.fit()
            elements += arima_results.predict()
        elements = elements / len(self.data)
        return self.run_information, [{"data": elements.tolist()}]
