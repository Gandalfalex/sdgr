import numpy as np
from keras.src.saving.saving_api import load_model
from matplotlib import pyplot as plt
import tensorflow as tf
from keras import layers, Sequential

from all_models_for_testing.general_ml_model import GeneralModel


class wgan(GeneralModel):
    input_length = 0
    latent_dim = 10

    def build_critic(self):
        model = Sequential()
        model.add(layers.Input(shape=(self.input_length, 1)))  # Expecting a sequence of length `input_length`
        model.add(layers.Conv1D(64, kernel_size=3, strides=1, padding="same"))
        model.add(layers.LeakyReLU(alpha=0.2))
        model.add(layers.Conv1D(128, kernel_size=3, strides=1, padding="same"))
        model.add(layers.LeakyReLU(alpha=0.2))
        model.add(layers.GlobalAveragePooling1D())
        model.add(layers.Dense(1))
        return model

    def build_generator(self):
        model = Sequential()
        model.add(layers.Input(shape=(self.latent_dim,)))
        model.add(layers.Dense(128 * self.input_length))  # Adjusted to produce a longer sequence
        model.add(layers.Reshape((self.input_length, 128)))
        model.add(layers.Conv1DTranspose(64, kernel_size=3, strides=1, padding="same"))
        model.add(layers.LeakyReLU(alpha=0.2))
        model.add(layers.Conv1DTranspose(1, kernel_size=3, strides=1, padding="same", activation="tanh"))
        model.add(layers.Reshape((self.input_length, 1)))  # Ensure the output shape is (input_length, 1)
        return model

    def train_step(self, real_data, generator, discriminator, g_optimizer, d_optimizer):
        batch_size = tf.shape(real_data)[0]
        random_latent_vectors = tf.random.normal(shape=(batch_size, self.latent_dim))

        with tf.GradientTape() as tape:
            generated_data = generator(random_latent_vectors)
            fake_logits = discriminator(tf.expand_dims(generated_data, -1))  # Ensure the shape is (batch_size, sequence_length, 1)
            real_logits = discriminator(real_data)
            d_cost = fake_logits - real_logits
            d_gradient = tape.gradient(d_cost, discriminator.trainable_variables)
        d_optimizer.apply_gradients(zip(d_gradient, discriminator.trainable_variables))

        with tf.GradientTape() as tape:
            generated_data = generator(random_latent_vectors)
            gen_img_logits = discriminator(generated_data)
            g_loss = -tf.reduce_mean(gen_img_logits)
            gen_gradient = tape.gradient(g_loss, generator.trainable_variables)
        g_optimizer.apply_gradients(zip(gen_gradient, generator.trainable_variables))

        return {"d_loss": tf.reduce_mean(d_cost), "g_loss": g_loss}

    def run(self):
        """
        start running the training
        input data is already normalized, length is the same

        after training the model, save it as keras file
        :return: self.run_information
        """
        self.input_length = len(self.data[0])
        generator = self.build_generator()
        critic = self.build_critic()
        dataset = tf.data.Dataset.from_tensor_slices(self.data).batch(64)
        d_optimizer = tf.keras.optimizers.RMSprop(learning_rate=0.00002)
        g_optimizer = tf.keras.optimizers.RMSprop(learning_rate=0.00002)

        for i in range(self.run_information.get("iteration_max")):
            for real_data in dataset:
                loss_dict = self.train_step(tf.expand_dims(real_data, -1), generator, critic, g_optimizer, d_optimizer)


        generator.save("saved_models/{}.keras".format(self.run_information.get("uuid")))
        return self.run_information

    def predict_data_from_model(self):
        """
        only generate synthetic data, model
        load the real model and use it to produce data
        :return: a sequence of synthetic data
        """
        model = load_model(("saved_models/{}.keras".format(self.run_information.get("uuid"))))
        random_latent_vectors = tf.random.normal(shape=(10, self.latent_dim))
        generated_data = model.predict(random_latent_vectors)
        for i in generated_data:
            plt.plot(i)
        plt.plot(self.data[0])
        plt.show()
        return generated_data
