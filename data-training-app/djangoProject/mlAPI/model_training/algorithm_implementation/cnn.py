import keras
import numpy as np
from keras.layers import Conv1D
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import LSTM
from keras.layers import MaxPooling1D
from keras.layers import TimeDistributed
from keras.models import Sequential
from matplotlib import pyplot as plt
from numpy import array

from mlAPI.model_training.ml_model_general import GeneralMLModel
from mlAPI.websocket_callbacks.keras_specific_callback import KerasCallback


class CNN(GeneralMLModel):
    testLength = 0.7
    scaler = 0.5

    def create_dataset(self, sequence, n_steps: int):
        x, y = list(), list()
        for i in range(len(sequence) - n_steps):
            end_ix = i + n_steps
            seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
            x.append(seq_x)
            y.append(seq_y)
        return array(x), array(y)

    def train_and_predict(self, model, x, y):
        model.fit(x, y, epochs=self.run_information.get_iterations(), verbose=0, use_multiprocessing=True,
                  callbacks=[KerasCallback(self.run_information)])
        return model

    def build_model(self, running_steps, n_features):
        model = Sequential()
        model.add(TimeDistributed(Conv1D(filters=64, kernel_size=1, activation='relu'),
                                  input_shape=(None, running_steps, n_features)))
        model.add(TimeDistributed(MaxPooling1D(pool_size=2)))
        model.add(TimeDistributed(Flatten()))
        model.add(LSTM(50, activation='relu'))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        return model

    def run(self):
        length = int(len(self.data[0]) * self.testLength)
        steps = int(len(self.data[0]) * self.scaler)
        n_steps = steps // 4
        features = 1
        n_seq = 4
        model = self.build_model(n_steps, features)

        for data in self.data:
            x, y = self.create_dataset(data, steps)
            x = x.reshape((x.shape[0], n_seq, n_steps, features))
            model = self.train_and_predict(model, x, y)
        self.save(model)

    def predict_data_from_model(self):
        steps = int(len(self.data[0]) * self.scaler)
        data = self.data[0].tolist()
        X, y = self.create_dataset(data, steps)

        n_seq = 4
        running_steps = steps // 4
        X = X.reshape((X.shape[0], n_seq, running_steps, 1))
        print(X.shape)
        model = keras.models.load_model("saved_models/abcdefg.keras")
        yhat = model.predict(X, verbose=0)
        temp = [element for sublist in yhat for element in sublist]

        pred_data = np.array(self.data[0][200:])
        pred_data2 = np.array(self.data[2][:200])
        new_data = []
        new_data2 = []

        for i in range(100):
            tempdata = pred_data.reshape((1, 4, 50, 1))
            m = model.predict(tempdata)
            new_data.append(m[0][0])
            pred_data = pred_data.tolist()
            pred_data.pop(0)
            pred_data.append(m[0][0])
            pred_data = np.array(pred_data)

        for i in range(300):
            tempdata = pred_data2.reshape((1, 4, 50, 1))
            m = model.predict(tempdata)
            new_data2.append(m[0][0])
            pred_data2 = pred_data2.tolist()
            pred_data2.pop(0)
            pred_data2.append(m[0][0])
            pred_data2 = np.array(pred_data2)

        plt.plot([0] * 200 + new_data2)
        plt.plot([0] * 400 + new_data)
        # plt.plot(temp)
        plt.plot(self.data[0])
        plt.show()
