import keras
import numpy as np
from keras import Sequential
from keras.layers import LSTM, Dropout, Dense
from sklearn.preprocessing import MinMaxScaler

from mlAPI.model_training.ml_model_general import GeneralMLModel
from mlAPI.websocket_callbacks.base_callback import MLCallback
from mlAPI.websocket_callbacks.keras_specific_callback import KerasCallback
from shared.annotations.gather_runtime_data import save_model_to_db


class RNN(GeneralMLModel):
    """
    prediction  = input_length % 2
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    prediction = 0
    test_length = 0.3
    model = None
    callback = None

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
        model.fit(train_data, test_data, epochs=self.run_information.get_iterations(), batch_size=32,
                  callbacks=[KerasCallback(self.run_information)], use_multiprocessing=True)
        return model

    @save_model_to_db
    def run(self):
        scaled = self.scale_data(self.data[0])
        self.callback = MLCallback(self.run_information)
        self.prediction = int(self.test_length * self.run_information.get_input_length())
        x, y = self.reshape_data(scaled, self.prediction)
        model = self.build_model(x.shape[1])
        self.run_information.max_steps = len(self.data)
        for i in range(len(self.data)):
            scaled = self.scale_data(self.data[i])
            x, y = self.reshape_data(scaled, self.prediction)
            model = self.train(model, x, y)
            self.run_information.increment_step()

        try:
            self.save(model)
            self.create_image(self.data[0], self.predict_data(model),
                              "RNN after {} iterations".format(self.run_information.get_iterations()))
        except Exception as e:
            print(e)
        return self.run_information

    def forcast(self, size):
        name = self.run_information.get_uuid()
        model = keras.models.load_model(f"saved_models/{name}.keras")
        self.prediction = int(self.test_length * self.run_information.get_input_length())
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

    def predict_data(self, model):
        data = np.array(self.data[0])
        test = []
        for i in range(1, len(data)):
            test.append(data[i - 1: i])

        test = np.array(test)
        test = np.reshape(test, (len(data) - 1, 1))
        pred = model.predict(test)
        result = self.scaler.fit_transform(pred)
        return [element for sublist in result.tolist() for element in sublist]

    def predict_data_from_model(self):
        model = self.load_model()
        return self.predict_data(model)
