import numpy as np
from scipy.interpolate import CubicSpline

from all_models_for_testing.general_ml_model import GeneralModel


class CubicSplineElement(GeneralModel):

    def run(self, precision=False):
        if self.run_information.get_all:
            all_information = []
            for data in self.data:
                spline = CubicSpline(np.arange(len(data)), data)
                all_information.append([spline(j) for j in range(len(data))])

            self.run_information.set_prediction(all_information)
            return self.run_information


        elements = np.zeros(len(self.data[0]))
        for i in self.data:
            spline = CubicSpline(np.arange(len(i)), i)
            elements += np.array([spline(j) for j in range(len(i))])
        elements = elements/len(self.data)
        self.run_information.set_prediction(elements.tolist())
        return self.run_information
