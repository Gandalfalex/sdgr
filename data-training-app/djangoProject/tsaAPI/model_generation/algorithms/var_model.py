import numpy as np
import pandas as pd
import statsmodels.api as sm
from tsaAPI.model_generation.algorithms.tsd_model_general import GeneralTSDModel


class VARModel(GeneralTSDModel):
    def run(self, precision=False):
        df = pd.DataFrame(self.data).T
        model = sm.tsa.VAR(df)
        results = model.fit(maxlags=5, ic='aic')
        forecast = results.forecast(df.values[-results.k_ar:], steps=1)
        return self.run_information, [{"data": forecast.tolist()}]
