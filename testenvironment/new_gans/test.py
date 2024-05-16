from tensorflow import keras
from tensorflow.keras import layers

import tensorflow as tf
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import tsgm


batch_size = 128

latent_dim = 1
feature_dim = 1
seq_len = 100
output_dim = 1

generator_in_channels = latent_dim + output_dim
discriminator_in_channels = feature_dim + output_dim

architecture = tsgm.models.architectures.zoo["t-cgan_c4"](
    seq_len=seq_len, feat_dim=feature_dim,
    latent_dim=latent_dim, output_dim=output_dim)
discriminator, generator = architecture.discriminator, architecture.generator

X, y = tsgm.utils.gen_sine_const_switch_dataset(7, seq_len, 1, max_value=20, const=10)

scaler = tsgm.utils.TSFeatureWiseScaler((-1, 1))
X_train = scaler.fit_transform(X)


X_train = X_train.astype(np.float32)
print(X_train.shape)
y = y.astype(np.float32)

dataset = tf.data.Dataset.from_tensor_slices((X_train, y))
dataset = dataset.shuffle(buffer_size=1024).batch(batch_size)

cond_gan = tsgm.models.cgan.ConditionalGAN(
    discriminator=discriminator, generator=generator, latent_dim=latent_dim,
    temporal=True,
)
cond_gan.compile(
    d_optimizer=keras.optimizers.Adam(learning_rate=0.0001, beta_1=0.5),
    g_optimizer=keras.optimizers.Adam(learning_rate=0.0001, beta_1=0.5),
    loss_fn=keras.losses.BinaryCrossentropy(),
)

cond_gan.fit(dataset, epochs=1)

test = np.ones((1, 100))
generated_images = cond_gan.generator(keras.utils.to_categorical(test))

test = [float(element) for sublist in generated_images[0] for element in sublist]
print(test)
