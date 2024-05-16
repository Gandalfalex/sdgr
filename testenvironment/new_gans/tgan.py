import numpy as np

import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers

import tensorflow as tf

import tsgm

from all_models_for_testing.general_ml_model import GeneralModel


class TGANModel(GeneralModel):
    latent_dim = 64
    output_dim = 2
    feature_dim = 1
    seq_len = 100
    batch_size = 128

    generator_in_channels = latent_dim + output_dim
    discriminator_in_channels = feature_dim + output_dim


    def run(self):

        model = tsgm.models.timeGAN.TimeGAN(
            seq_len=len(self.data),
            module="gru",
            hidden_dim=24,
            n_features=len(self.data[0]),
            n_layers=3,
            batch_size=256,
            gamma=1.0,
        )
        # .compile() sets all optimizers to Adam by default
        model.compile()
        self.data = np.array(self.data).reshape(1, len(self.data), len(self.data[0]))
        model.fit(
            data=self.data,
            epochs=self.run_information.iterations,
        )

        try:
            m = self.predict_data(model)
            print(m)
            self.run_information.set_prediction(m)
        except Exception as e:
            print(e)
        return self.run_information

    def predict_data(self, model):
        test = model.generate(n_samples=100)
        i = [float(i) for i in test[0][0]]
        if self.run_information.get_all:
            all = []
            for element in test:
                all.append([float(j) for j in element])
            return all
        return i


