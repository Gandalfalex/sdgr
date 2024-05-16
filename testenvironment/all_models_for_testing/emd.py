import emd
import numpy as np

from all_models_for_testing.general_ml_model import GeneralModel

"""
https://emd.readthedocs.io/en/stable/emd_tutorials/01_sifting/emd_tutorial_01_sift_02_siftindetail.html
"""


class EmpiricalModeDecomposition(GeneralModel):
    imf = None

    def run(self, precision=False):
        if self.run_information.get_all:
            all_information = []
            for data in self.data:
                m = np.array(data).reshape((-1,))
                self.imf = emd.sift.mask_sift(m, max_imfs=self.run_information.split)
                all_information.append(self.sum_up_data())
            self.run_information.set_prediction(all_information)
            return self.run_information

        x = self.data[0].tolist()
        m = np.array(x).reshape((-1, ))

        self.imf = emd.sift.mask_sift(m, max_imfs=self.run_information.split)

        self.run_information.set_prediction(self.sum_up_data())
        return self.run_information


    def sum_up_data(self):
        max_depth = min(self.run_information.precision, len(self.imf[0]))
        sum_data = np.zeros(len(self.data[0]))
        for i in range(len(self.imf)):
            sum_data[i] = sum(self.imf[i][:max_depth-1])
        return sum_data.tolist()