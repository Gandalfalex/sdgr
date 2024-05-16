import emd

from tsaAPI.model_generation.algorithms.tsd_model_general import GeneralTSDModel

"""
https://emd.readthedocs.io/en/stable/emd_tutorials/01_sifting/emd_tutorial_01_sift_02_siftindetail.html
"""


class EmpiricalModeDecomposition(GeneralTSDModel):
    imf = None

    def run(self, precision=False):
        self.data = self.data.reshape((-1, ))
        self.imf = emd.sift.mask_sift(self.data, max_imfs=self.run_information.split)
        data = self.create_returnable_data(self.imf, precision)
        return self.run_information, data


    def sum_up_data(self):
        x = 1
        sum_data = [0] * len(x)
        for i in range(len(x)):
            for j in range(1, len(self.imf[0])):
                sum_data[i] = sum_data[i] + self.imf[i][j]

        sum_data = self.add_linear_trend(sum_data, 0)
        return sum_data