import numpy as np
import statsmodels.api as sm

from all_models_for_testing.general_ml_model import GeneralModel


class AmiraModel(GeneralModel):

    def run(self, precision=False):
        if self.run_information.get_all:
            all_information = []
            for data in self.data:
                arima_model = sm.tsa.arima.ARIMA(data, order=(1, 1, 1))
                arima_results = arima_model.fit()
                all_information.append(list(arima_results.predict()))
            self.run_information.set_prediction(all_information)
            return self.run_information

        elements = np.zeros(len(self.data[0]))
        for i in self.data:
            arima_model = sm.tsa.arima.ARIMA(i, order=(1, 1, 1))
            arima_results = arima_model.fit()
            elements += arima_results.predict()
        elements = elements / len(self.data)
        self.run_information.set_prediction(elements.tolist())
        return self.run_information
