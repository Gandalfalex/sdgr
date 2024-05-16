import numpy as np
from keras import backend as K, Model, Input
from keras.layers import Dense
from keras.optimizers import RMSprop
from keras.src.layers import Concatenate, BatchNormalization, LSTM, Reshape, RepeatVector
from keras.src.optimizers import Adam
from keras.src.saving.saving_api import load_model
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from models_for_testing.ml_model_general import GeneralMLModel


class tgan(GeneralMLModel):
    latent_dim = 5
    n_features = 1
    n_outputs = 0
    def define_generator(self, latent_dim, n_outputs):
        in_noise = Input(shape=(latent_dim,))
        in_label = Input(shape=(1,))
        merge = Concatenate()([in_noise, in_label])
        model = Dense(150, activation='relu')(merge)
        model = Reshape((1, 150))(model)  # Reshape for LSTM
        model = LSTM(50, return_sequences=True)(model)
        model = LSTM(n_outputs * self.n_features, return_sequences=True)(model)
        model = Reshape((n_outputs, self.n_features))(model)
        return Model([in_noise, in_label], model)

    def define_discriminator(self, sequence_length):
        in_sample = Input(shape=(sequence_length, self.n_features))
        in_label = Input(shape=(1,))

        label_repeated = RepeatVector(sequence_length)(in_label)
        label_repeated = Reshape((sequence_length, 1))(label_repeated)

        merge = Concatenate(axis=-1)([in_sample, label_repeated])

        model = LSTM(250, activation='relu', return_sequences=True)(merge)
        model = LSTM(100, activation='relu')(model)
        model = Dense(1, activation='sigmoid')(model)

        model = Model([in_sample, in_label], model)
        model.compile(loss='binary_crossentropy', optimizer=Adam(), metrics=['accuracy'])
        return model

    def generate_real_samples(self, dataset, n_samples, sequence_length):
        ix = np.random.randint(0, dataset.shape[0], n_samples)
        X = dataset[ix]
        X = X.reshape((n_samples, sequence_length, self.n_features))
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
        x_input = np.random.randn(latent_dim * n_samples)
        z_input = x_input.reshape(n_samples, latent_dim)
        labels = np.random.randint(0, n_classes, n_samples).reshape(n_samples, 1)
        return [z_input, labels]

    # train the discriminator model
    def train(self, g_model, d_model, gan_model, latent_dim, data, n_batch=128):
        half_batch = int(n_batch / 2)
        for i in range(self.run_information.get("iteration_max")):
            [X_real, labels_real], y_real = self.generate_real_samples(data, half_batch, self.n_outputs)
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
        self.n_outputs = len(self.data[0])
        self.n_features = 1
        discriminator = self.define_discriminator(self.n_outputs)
        generator = self.define_generator(latent_dim, self.n_outputs)
        gan_model = self.define_gan(generator, discriminator)
        data = np.vstack(self.data)
        model = self.train(generator, discriminator, gan_model, latent_dim, data)
        model.save("saved_models/{}.keras".format(self.run_information.get("uuid")))

    def predict_data_from_model(self):
        data = np.vstack(self.data)
        model = load_model("saved_models/{}.keras".format(self.run_information.get("uuid")), compile=False)
        m = self.generate_synthetic_data(model, self.latent_dim, len(data[0]))
        plt.plot(m[0])
        plt.plot(m[3])
        plt.plot(m[4])
        plt.plot(self.data[1])
        plt.show()

    def generate_synthetic_data(self, generator, latent_dim, n_samples):
        z_input, labels_input = self.generate_latent_points(latent_dim, n_samples)
        # Predict synthetic samples
        synthetic_samples = generator.predict([z_input, labels_input])
        return synthetic_samples