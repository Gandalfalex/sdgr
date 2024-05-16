import keras
import numpy as np
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler

from models_for_testing.ml_model_general import GeneralMLModel


class LongShortTermMemory(GeneralMLModel):
    test_length = 0.2
    scaler = MinMaxScaler()
    recreation_limit = 100

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
        model.fit(x_train, y_train, epochs=self.run_information.get("iteration_max"),
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

        for data in self.data:
            x_train, y_train = self.preprocess_data(data)
            model = self.run_lstm(x_train, y_train, model)

        model.save("saved_models/{}.keras".format(self.run_information.get("uuid")))

    def forcast(self, size):
        train_size = int(len(self.data[0]) * self.test_length)
        pred_data = self.data[0][:train_size]
        model = keras.models.load_model("saved_models/{}.keras".format(self.run_information.get("uuid")))
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

    def predict_data_from_model(self):
        x = self.data[0]
        scaler = MinMaxScaler()

        model = keras.models.load_model("saved_models/{}.keras".format(self.run_information.get("uuid")))

        data = x.reshape(len(x), 1)
        temp = model.predict(data)

        temp = scaler.fit_transform(temp)
        temp = [element for sublist in temp for element in sublist]
        return temp

