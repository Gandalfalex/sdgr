import logging
import math

import numpy as np
from keras import Input
from keras.layers import Dense, LSTM
from keras.models import Sequential
from numpy import ones
from numpy import zeros
from numpy.random import randn
from statsmodels.tsa.api import SimpleExpSmoothing

from all_models_for_testing.general_ml_model import GeneralModel


class GAN(GeneralModel):
    latent_dim = 3

    def define_discriminator(self):
        model = Sequential()
        model.add(Dense(self.run_information.get_input_length(), activation='relu',
                        input_dim=self.run_information.get_input_length()))
        model.add(Dense(250, activation='relu', input_dim=self.run_information.get_input_length()))
        model.add(Dense(150, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

    def define_generator(self, latent_dim):
        model = Sequential()
        model.add(Input(shape=(latent_dim, 1)))
        model.add(LSTM(150))
        model.add(Dense(self.run_information.get_input_length(), activation='linear'))
        model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mean_absolute_error'])
        return model

    # define the combined generator and discriminator model, for updating the generator
    def define_gan(self, generator, discriminator):
        discriminator.trainable = False
        model = Sequential()
        model.add(generator)
        model.add(discriminator)
        model.compile(loss='binary_crossentropy', optimizer='adam')
        return model

    # generate n real samples with class labels
    def get_real_samples(self, n):
        indices = np.random.choice(self.data.shape[0], size=n, replace=False)
        x1 = self.data[indices]
        y = ones((n, 1))
        return x1, y

    # generate points in latent space as input for the generator, y points are labels
    def generate_latent_points(self, latent_dim, n):
        x_input = randn(latent_dim * n)
        x_input = x_input.reshape(n, latent_dim)
        return x_input

    # use the generator to generate n fake examples, with class labels
    def generate_fake_samples(self, generator, latent_dim, n):
        x_input = self.generate_latent_points(latent_dim, n)
        x = generator.predict(x_input, verbose=0, use_multiprocessing=True)
        y = zeros((n, 1))
        return x, y

    # train the generator and discriminator
    def train(self, g_model, d_model, gan_model, latent_dim, n_batch=64, n_eval=100):
        # determine half the size of one batch, for updating the discriminator
        half_batch = int(n_batch / 2)
        # manually enumerate epochs
        for i in range(self.run_information.get_iterations()):
            x_real, y_real = self.get_real_samples(latent_dim)
            x_fake, y_fake = self.generate_fake_samples(g_model, latent_dim, half_batch)
            d_model.train_on_batch(x_real, y_real)
            d_model.train_on_batch(x_fake, y_fake)
            x_gan = self.generate_latent_points(latent_dim, n_batch)
            y_gan = ones((n_batch, 1))
            gan_model.train_on_batch(x_gan, y_gan)
        return g_model


    def run(self):
        latent_dim = 3
        m = self.calculate_batch_size()
        generator = self.define_generator(latent_dim)
        discriminator = self.define_discriminator()
        gan_model = self.define_gan(generator, discriminator)
        try:
            model = self.train(generator, discriminator, gan_model, latent_dim, m)

            m = self.predict_data(model)
            self.run_information.set_prediction(m)
            self.run_information.set_loss(model.loss)
        except Exception as e:
            logging.error(e)
        return self.run_information

    def calculate_batch_size(self):
        x = math.log2(self.data.shape[0])
        x = math.ceil(x)
        return int(math.pow(2, x))

    def predict_data_from_model(self):
        model = self.load_model()
        return self.predict_data(model)

    def predict_data(self, model):
        n = self.calculate_batch_size()
        x_input = self.generate_latent_points(3, n)
        data = model.predict(x_input, verbose=0, use_multiprocessing=True)

        if self.run_information.get_all:
            all = []
            for i in data:
                smoother = SimpleExpSmoothing(i)
                smoothed_time_series = smoother.fit(method="basinhopping", smoothing_level=0.3,
                                                    optimized=True).fittedvalues
                all.append(smoothed_time_series.tolist())
            return all

        smoother = SimpleExpSmoothing(data[0])
        smoothed_time_series = smoother.fit(method="basinhopping", smoothing_level=0.3, optimized=True).fittedvalues
        return smoothed_time_series.tolist()
