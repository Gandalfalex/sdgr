import numpy as np

import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers

import tensorflow as tf

import tsgm

from all_models_for_testing.general_ml_model import GeneralModel


class TCGANModel(GeneralModel):
    batch_size = 128

    latent_dim = 1
    feature_dim = 1
    seq_len = 100
    output_dim = 1

    def convert_data(self, data, min_scale=0, max_scale=1, buffer_size=1024, batch_size=32):
        X = np.array(data).reshape((7, 100, 1))

        y = np.ones((7, 100))
        X_train = X.astype(np.float32)
        y = y.astype(np.float32)

        tf_dataset = tf.data.Dataset.from_tensor_slices((X_train, y))
        tf_dataset = tf_dataset.shuffle(buffer_size).batch(batch_size)

        return tf_dataset

    def run(self):

        architecture = tsgm.models.architectures.zoo["t-cgan_c4"](
            seq_len=self.seq_len, feat_dim=self.feature_dim,
            latent_dim=self.latent_dim, output_dim=self.output_dim)
        discriminator, generator = architecture.discriminator, architecture.generator

        cond_gan = tsgm.models.cgan.ConditionalGAN(
            discriminator=discriminator, generator=generator, latent_dim=self.latent_dim,
            temporal=True,
        )
        cond_gan.compile(
            d_optimizer=keras.optimizers.Adam(learning_rate=0.0001, beta_1=0.5),
            g_optimizer=keras.optimizers.Adam(learning_rate=0.0001, beta_1=0.5),
            loss_fn=keras.losses.BinaryCrossentropy(),
        )

        dataset = self.convert_data(self.data)
        cond_gan.fit(dataset, epochs=self.run_information.iterations)
        try:
            m = self.predict_data(cond_gan)
            self.run_information.set_prediction(m)
        except Exception as e:
            print(e)
        return self.run_information

    def predict_data(self, model):
        test = np.ones((7, 100))

        generated_images = model.generator(keras.utils.to_categorical(test))

        if self.run_information.get_all:
            all = []
            for i in generated_images:
                all.append([float(sublist) for sublist in i])
            return all

        test = [float(element) for sublist in generated_images[0] for element in sublist]
        return test
