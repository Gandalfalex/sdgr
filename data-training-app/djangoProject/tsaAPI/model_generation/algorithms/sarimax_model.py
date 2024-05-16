import numpy as np
import statsmodels.api as sm
from tsaAPI.model_generation.algorithms.tsd_model_general import GeneralTSDModel


class SARIMAXModel(GeneralTSDModel):
    def run(self, precision=False, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12), exog=None):
        elements = np.zeros(len(self.data[0]))
        for i in self.data:
            print(i)
            sarimax_model = sm.tsa.SARIMAX(i, order=order, seasonal_order=seasonal_order, exog=exog)
            sarimax_results = sarimax_model.fit()
            print(sarimax_results.predict())
            elements += sarimax_results.predict()
        elements = elements / len(self.data)
        return self.run_information, [{"data": elements.tolist()}]
