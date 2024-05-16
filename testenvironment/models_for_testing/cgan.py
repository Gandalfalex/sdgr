import base64
from io import BytesIO

import numpy as np
from keras.models import load_model
from keras.models import Sequential, Model
from keras.layers import Dense, Input, Concatenate
from keras.src.optimizers import Adam
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

from models_for_testing.ml_model_general import GeneralMLModel


class cgan(GeneralMLModel):

    def define_generator(self, latent_dim, n_outputs):
        in_noise = Input(shape=(latent_dim,))
        in_label = Input(shape=(1,))
        merge = Concatenate()([in_noise, in_label])

        model = Dense(150, activation='relu')(merge)
        model = Dense(n_outputs, activation='sigmoid')(model)

        model = Model([in_noise, in_label], model)
        return model

    def define_discriminator(self, n_inputs):
        in_sample = Input(shape=(n_inputs,))
        in_label = Input(shape=(1,))
        merge = Concatenate()([in_sample, in_label])

        model = Dense(250, activation='relu')(merge)
        model = Dense(1, activation='sigmoid')(model)

        model = Model([in_sample, in_label], model)
        model.compile(loss='binary_crossentropy', optimizer=Adam(), metrics=['accuracy'])
        return model

    # generate n real samples with class labels
    def generate_real_samples(self, dataset, n_samples):
        ix = np.random.randint(0, dataset.shape[0], n_samples)
        X = dataset[ix]
        y = np.ones((n_samples, 1))
        labels = np.ones((n_samples, 1))  # Assuming label 1 for real samples
        return [X, labels], y

    # generate n fake samples with class labels
    def generate_fake_samples(self, generator, latent_dim, n_samples):
        z_input, labels_input = self.generate_latent_points(latent_dim, n_samples)
        images = generator.predict([z_input, labels_input])
        y = np.zeros((n_samples, 1))
        return [images, labels_input], y

    # Generate points in latent space as input for the generator
    def generate_latent_points(self, latent_dim, n_samples, n_classes=2):
        # Generate random noise
        x_input = np.random.randn(latent_dim * n_samples)
        z_input = x_input.reshape(n_samples, latent_dim)
        # Generate labels
        labels = np.random.randint(0, n_classes, n_samples).reshape(n_samples, 1)
        return [z_input, labels]

    # train the discriminator model
    def train(self, g_model, d_model, gan_model, latent_dim, data, n_batch=128):
        half_batch = int(n_batch / 2)
        for i in range(self.run_information.get("iteration_max")):
            [X_real, labels_real], y_real = self.generate_real_samples(data, half_batch)
            d_loss1, _ = d_model.train_on_batch([X_real, labels_real], y_real)

            [X_fake, labels_fake], y_fake = self.generate_fake_samples(g_model, latent_dim, half_batch)
            d_loss2, _ = d_model.train_on_batch([X_fake, labels_fake], y_fake)

            [z_input, z_labels] = self.generate_latent_points(latent_dim, n_batch)
            y_gan = np.ones((n_batch, 1))
            g_loss = gan_model.train_on_batch([z_input, z_labels], y_gan)
        return g_model

    def define_gan(self, generator, discriminator):
        discriminator.trainable = False
        gen_noise, gen_label = generator.input
        gen_output = generator.output
        gan_output = discriminator([gen_output, gen_label])
        model = Model([gen_noise, gen_label], gan_output)
        model.compile(loss='binary_crossentropy', optimizer=Adam())
        return model

    def run(self):
        latent_dim = 5
        discriminator = self.define_discriminator(len(self.data[0]))
        generator = self.define_generator(latent_dim, len(self.data[0]))
        gan_model = self.define_gan(generator, discriminator)
        m = MinMaxScaler()
        n = m.fit_transform(self.data.reshape(-1, 1)).reshape(len(self.data), len(self.data[0]))
        data = np.vstack(n)
        model = self.train(generator, discriminator, gan_model, latent_dim, data)
        self.create_image(self.data[0], self.predict_data_from_model(),
                          "GAN with {}".format(self.run_information.get("iteration_max")))
        model.save("saved_models/{}.keras".format(self.run_information.get("uuid")))

    def predict_data_from_model(self):
        scaler = MinMaxScaler()
        n = scaler.fit_transform(self.data.reshape(-1, 1)).reshape(len(self.data), len(self.data[0]))
        data = np.vstack(n)
        model = load_model("saved_models/{}.keras".format(self.run_information.get("uuid")), compile=False)
        m = self.generate_synthetic_data(model, 5, len(data[0]))
        smoother = SimpleExpSmoothing(m[0])
        smoothed_time_series = smoother.fit(method="basinhopping", smoothing_level=0.3, optimized=True).fittedvalues
        return smoothed_time_series

    def generate_synthetic_data(self, generator, latent_dim, n_samples):
        z_input, labels_input = self.generate_latent_points(latent_dim, n_samples)
        synthetic_samples = generator.predict([z_input, labels_input])
        return synthetic_samples

    def forcast(self):
        pass


    def create_image(self, original: [], predicted: [], title: str):
        try:
            plt.title(title)
            plt.plot(original, label="original")
            plt.plot(predicted, label="created")
            plt.legend()
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()

            base64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            print(base64_str)
            self.run_information["image"] = base64_str
        except Exception as e:
            print(e)