import numpy as np
from keras import Sequential
from keras.src.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

from all_models_for_testing.general_ml_model import GeneralModel


class LSTM_custom(GeneralModel):
    test_length = 0.7
    train_ratio = 0.7
    scaler = MinMaxScaler()

    def create_dataset(self, data, time_step: int):
        data_x, data_y = [], []
        for i in range(len(data) - time_step):
            a = data[i:(i + time_step)]
            data_x.append(a)
            data_y.append(data[i + time_step])
        return np.array(data_x), np.array(data_y)

    def preprocess_data(self, data):
        train_size = int(len(data) * self.test_length)
        x_train, y_train = self.create_dataset(data, train_size)
        return x_train, y_train

    def run_lstm(self, x_train, y_train, model):
        model.fit(x_train, y_train, epochs=self.run_information.get_iterations(),
                  batch_size=64, verbose=0)
        return model

    def run(self):
        x_train, _ = self.preprocess_data(self.data[0])
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(50, return_sequences=True))
        model.add(LSTM(50))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')

        for i, data in enumerate(self.data):
            x_train, y_train = self.preprocess_data(data)
            model = self.run_lstm(x_train, y_train, model)

        if self.run_information.forcast:
            self.run_information.set_forcast(self.forcast(100, model))
        else:
            prediction = self.predict_data(model)
            self.run_information.set_loss(model.loss)
            self.run_information.set_prediction(prediction)
        return self.run_information

    def forcast(self, size, model):
        train_size = int(len(self.data[0]) * self.test_length)
        pred_data = self.data[0][-train_size:]

        new_data = []
        for i in range(size):
            tempdata = pred_data.reshape((1, train_size, 1))
            m = model.predict(tempdata, verbose=0)
            new_data.append(m[0][0])
            pred_data = pred_data.tolist()
            pred_data.pop(0)
            pred_data.append(m[0][0])
            pred_data = np.array(pred_data)

        return [float(i) for i in new_data]

    def predict_data(self, model):
        if self.run_information.get_all:
            all_data = []
            length_data = len(self.data[0])
            for data in self.data:
                scaler = MinMaxScaler()

                data = data.reshape(length_data, 1)
                temp = model.predict(data)
                temp = scaler.fit_transform(temp)
                all_data.append([element for sublist in temp for element in sublist])
            return all_data

        test_on = self.data[0]
        scaler = MinMaxScaler()

        data = test_on.reshape(len(test_on), 1)

        temp = model.predict(data)
        temp = scaler.fit_transform(temp)
        temp = [element for sublist in temp for element in sublist]
        return temp

    def predict_data_from_model(self):
        model = self.load_model()
        return self.predict_data(model)
