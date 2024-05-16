import keras
import numpy as np
from keras import Sequential
from keras.layers import LSTM, Dropout, Dense
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from models_for_testing.ml_model_general import GeneralMLModel


class RNN_2(GeneralMLModel):
    """
    prediction  = input_length % 2
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    prediction = 0
    test_length = 0.2
    model = None
    recreation_limit = 100

    def scale_data(self, data):
        scaled_data = self.scaler.fit_transform(data.reshape(-1, 1))
        return scaled_data

    def reshape_data(self, data, steps):
        X, y = list(), list()
        for i in range(len(data) - steps):
            end_ix = i + steps
            seq_x, seq_y = data[i:end_ix], data[end_ix]
            X.append(seq_x)
            y.append(seq_y)
        return np.array(X), np.array(y)

    def build_model(self, shape: int):
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(shape, 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))
        model.compile(optimizer="adam", loss="mean_squared_error")
        return model

    def train(self, model, train_data, test_data):
        model.fit(train_data, test_data, epochs=self.run_information.get("iteration_max"), batch_size=32,
                  use_multiprocessing=True, verbose=0)
        return model

    def run(self):
        scaled = self.scale_data(self.data[0])
        self.prediction = int(self.test_length * self.run_information.get("input_length"))
        x, y = self.reshape_data(scaled, self.prediction)
        model = self.build_model(x.shape[1])

        for data in self.data:
            scaled = self.scale_data(data)
            x, y = self.reshape_data(scaled, self.prediction)
            model = self.train(model, x, y)

        model.save("saved_models/{}.keras".format(self.run_information.get("uuid")))

        return self.run_information

    def plot(self, original, created):
        plt.plot(original, color="black", label="actual_data")
        plt.plot(created, color="red", label="predicted data")
        plt.show()

    def forcast(self, size):
        name = self.run_information.get("uuid")
        model = keras.models.load_model(f"saved_models/{name}.keras")
        self.prediction = int(self.test_length * self.run_information.get("input_length"))
        data = self.data[0][: self.prediction]
        pred_data = self.scaler.fit_transform(data.reshape(-1, 1))
        new_data = []
        for i in range(size):
            tempdata = pred_data.reshape(1, self.prediction, 1)
            m = model.predict(tempdata, verbose=0)
            new_data.append(m[0])
            pred_data = pred_data.tolist()
            pred_data.pop(0)
            pred_data.append(m[0])
            pred_data = np.array(pred_data)

        result = self.scaler.inverse_transform(new_data)

        return [float(element) for sublist in result.tolist() for element in sublist]

    def predict_data_from_model(self):
        name = self.run_information.get("uuid")
        model = keras.models.load_model(f"saved_models/{name}.keras")
        data = np.array(self.data[0])
        test = []
        for i in range(1, len(data)):
            test.append(data[i - 1: i])

        test = np.array(test)
        test = np.reshape(test, (len(data) - 1, 1))
        pred = model.predict(test)
        result = self.scaler.fit_transform(pred)
        return [element for sublist in result.tolist() for element in sublist]