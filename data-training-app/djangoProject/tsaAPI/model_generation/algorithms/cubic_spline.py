import numpy as np
from scipy.interpolate import CubicSpline
from tsaAPI.model_generation.algorithms.tsd_model_general import GeneralTSDModel


class CubicSplineElement(GeneralTSDModel):

    def run(self, precision=False):
        elements = np.zeros(len(self.data[0]))
        for i in self.data:
            spline = CubicSpline(np.arange(len(i)), i)
            elements += np.array([spline(j) for j in range(len(i))])
        elements = elements/len(self.data)
        return self.run_information, [{"data": elements.tolist()}]
