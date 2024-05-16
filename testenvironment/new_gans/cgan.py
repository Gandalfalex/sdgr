import numpy as np

import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers

import tensorflow as tf

import tsgm

from all_models_for_testing.general_ml_model import GeneralModel


class CGANModel(GeneralModel):
    latent_dim = 64
    output_dim = 2
    feature_dim = 1
    seq_len = 100
    batch_size = 128

    generator_in_channels = latent_dim + output_dim
    discriminator_in_channels = feature_dim + output_dim

    def convert_data(self, data, min_scale=0, max_scale=1, buffer_size=1024, batch_size=32):
        # Assuming data is an array of arrays
        ts_len = len(data[0])  # The length of each time series
        print(len(data), ts_len)
        X = np.array(data).reshape(-1, ts_len, 1)

        # Scale the data
        scaler = tsgm.utils.TSFeatureWiseScaler((min_scale, max_scale))
        X_train = scaler.fit_transform(X)
        y = keras.utils.to_categorical(np.ones(len(data)), 2)
        X_train = X_train.astype(np.float32)
        y = y.astype(np.float32)

        # Create a tensorflow data set
        tf_dataset = tf.data.Dataset.from_tensor_slices((X_train, y))
        tf_dataset = tf_dataset.shuffle(buffer_size).batch(batch_size)

        return tf_dataset

    def run(self):
        architecture = tsgm.models.architectures.zoo["cgan_base_c4_l1"](
            seq_len=len(self.data[0]), feat_dim=self.feature_dim,
            latent_dim=self.latent_dim, output_dim=self.output_dim)
        discriminator, generator = architecture.discriminator, architecture.generator
        cond_gan = tsgm.models.cgan.ConditionalGAN(
            discriminator=discriminator, generator=generator, latent_dim=self.latent_dim
        )
        cond_gan.compile(
            d_optimizer=keras.optimizers.Adam(learning_rate=0.0002, beta_1=0.5),
            g_optimizer=keras.optimizers.Adam(learning_rate=0.0002, beta_1=0.5),
            loss_fn=keras.losses.BinaryCrossentropy(),
        )
        dataset = self.convert_data(self.data)
        cond_gan.fit(dataset, epochs=self.run_information.iterations)
        try:
            pred = self.predict_data(cond_gan)
            self.run_information.set_loss(cond_gan.loss)
            self.run_information.set_prediction(pred)
        except Exception as e:
            print(e)
        return self.run_information

    def predict_data(self, model):
        X_gen = model.generate(keras.utils.to_categorical(np.ones(len(self.data)), 2))
        test = X_gen.numpy()
        all = []
        if self.run_information.get_all:
            for i in test:
                all.append([float(element) for sublist in i.tolist() for element in sublist])
            return all
        test = [float(element) for sublist in test[0].tolist() for element in sublist]
        return test

