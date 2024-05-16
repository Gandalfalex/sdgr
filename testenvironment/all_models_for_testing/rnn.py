import keras
import numpy as np
from keras import Sequential
from keras.layers import LSTM, Dropout, Dense
from keras.src.models import clone_model
from sklearn.preprocessing import MinMaxScaler

from all_models_for_testing.general_ml_model import GeneralModel


class RNN(GeneralModel):
    """
    prediction  = input_length % 2
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    prediction = 0
    test_length = 0.7
    train_ratio = 0.7
    model = None

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
                  use_multiprocessing=True)
        return model

    def run(self):
        scaled = self.scale_data(self.data[0])
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
            if self.run_information.forcast:
                self.run_information.set_forcast(self.forcast2(100, model, self.data[0]))
            else:
                prediction = self.predict_data(model)
                self.run_information.set_loss(model.loss)
                self.run_information.set_prediction(prediction)

        except Exception as e:
            print(e)
        return self.run_information

    def forcast(self, limit: int, model, data):
        self.prediction = int(self.test_length * self.run_information.get_input_length())

        data = data[-self.prediction:]
        pred_data = self.scaler.fit_transform(data.reshape(-1, 1))
        new_data = []
        for i in range(limit):
            tempdata = pred_data.reshape(1, self.prediction, 1)
            m = model.predict(tempdata, verbose=0)
            new_data.append(m[0])
            pred_data = pred_data.tolist()
            pred_data.pop(0)
            pred_data.append(m[0])
            pred_data = np.array(pred_data)
        result = self.scaler.inverse_transform(new_data)
        return [float(element) for sublist in result.tolist() for element in sublist]

    def run_prediction_for_all(self, model):
        all_data = []
        length_data = len(self.data[0])
        for data in self.data:
            second = clone_model(model)
            data_ = data.reshape(len(data), 1)
            test = []
            for i in range(1, len(data_)):
                test.append(data_[i - 1: i])

            test = np.array(test)
            test = np.reshape(test, (data_ - 1, 1))
            pred = second.predict(test)

            result = self.scaler.fit_transform(pred)
            last_value = self.forcast(1, second, data)
            all_data.append([element for sublist in result.tolist() for element in sublist] + last_value)
        return all_data

    def predict_data(self, model):
        if self.run_information.get_all:
            return self.run_prediction_for_all(model)

        second = clone_model(model)
        test_on = self.data[0]
        data = test_on.reshape(len(test_on), 1)

        test = []
        for i in range(1, len(data)):
            test.append(data[i - 1: i])

        test = np.array(test)
        test = np.reshape(test, (len(data) - 1, 1))
        pred = model.predict(test)
        result = self.scaler.fit_transform(pred)
        last_value = self.forcast(1, second, data)
        test = [element for sublist in result.tolist() for element in sublist]
        return test + last_value
