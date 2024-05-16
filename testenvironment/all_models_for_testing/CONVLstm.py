import keras
import numpy as np
from keras.layers import Dense
from keras.layers import Flatten
from keras.models import Sequential
from keras.src.layers import ConvLSTM2D
from numpy import array
from sklearn.preprocessing import MinMaxScaler

from all_models_for_testing.general_ml_model import GeneralModel


class CONVLstm(GeneralModel):
    test_length = 0.7
    train_ratio = 0.7
    recreation_limit = 100
    scaler = MinMaxScaler(feature_range=(0, 1))

    def create_dataset(self, data, n_steps: int):
        x, y = list(), list()
        for i in range(len(data) - n_steps):
            end_ix = i + n_steps
            seq_x, seq_y = data[i:end_ix], data[end_ix]
            x.append(seq_x)
            y.append(seq_y)
        return array(x), array(y)

    def train_and_predict(self, model, x, y):
        model.fit(x, y, epochs=self.run_information.get_iterations(), verbose=0, use_multiprocessing=True)
        return model

    def build_model(self, sequence, running_steps, n_features):
        model = Sequential()
        model.add(ConvLSTM2D(filters=64, kernel_size=(1, 2), activation='relu',
                             input_shape=(sequence, 1, running_steps, n_features)))
        model.add(Flatten())
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        return model

    def run(self):
        steps = int(len(self.data[0]) * self.test_length)
        n_steps, n_seq = self.calc_param(steps)
        features = 1

        model = self.build_model(n_seq, n_steps, features)

        for data in self.data:
            x, y = self.create_dataset(data, steps)
            x = x.reshape((x.shape[0], n_seq, 1, n_steps, features))
            model = self.train_and_predict(model, x, y)

        if self.run_information.forcast:
            self.run_information.set_forcast(self.forcast(100, model))
        else:
            prediction = self.predict_data(model)
            self.run_information.set_loss(model.loss)
            self.run_information.set_prediction(prediction)
        return self.run_information

    def run_prediction(self, model, data):
        steps = int(len(data) * self.test_length)
        n_steps, n_seq = self.calc_param(steps)
        features = 1

        new_data = []
        pred_data = data[:steps]

        for i in range(self.recreation_limit):
            tempdata = pred_data.reshape((1, n_seq, 1, n_steps, features))
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
            for data in self.data:
                all_data.append(self.run_prediction(model, data))
            return all_data
        return self.run_prediction(model, self.data[0])

    def predict_data_from_model(self):
        model = keras.models.load_model("saved_models/abcdefg.keras")
        return self.predict_data(model)

    def calc_param(self, steps):
        options = self.prime_factors(steps)
        temp_options = []
        for o in options:
            if o not in temp_options:
                temp_options.append(o)
        sums = [pow(n, options.count(n)) for n in temp_options]
        if len(sums) == 1:
            n_seq = options[0]
            n_steps = 1
            for l in options[1:]:
                n_steps = l * n_steps
        else:
            n_seq = sums[0]
            n_steps = 1
            for l in sums[1:]:
                n_steps = l * n_steps
        return n_steps, n_seq

    def prime_factors(self, n):
        factors = []

        while n % 2 == 0:
            factors.append(2)
            n //= 2

        for i in range(3, int(n ** 0.5) + 1, 2):
            while n % i == 0:
                factors.append(i)
                n //= i

        if n > 2:
            factors.append(n)

        return factors


    def forcast(self, limit: int, model) -> []:
        steps = int(len(self.data[0]) * self.test_length)
        n_steps, n_seq = self.calc_param(steps)
        last = self.data[0][-1]
        self.prediction = int(self.test_length * self.run_information.get_input_length())
        data = self.data[0][-(n_seq * n_steps):]
        pred_data = self.scaler.fit_transform(data.reshape(-1, 1))
        new_data = []
        for i in range(limit):
            tempdata = pred_data.reshape(1, n_seq, 1, n_steps, 1)
            m = model.predict(tempdata, verbose=1)
            new_data.append(m[0])
            pred_data = pred_data.tolist()
            pred_data.pop(0)
            pred_data.append(m[0])
            pred_data = np.array(pred_data)
        result = self.scaler.inverse_transform(new_data)
        result = [float(element) for sublist in result.tolist() for element in sublist]
        last_res = last - result[0]
        result = [i + last_res for i in result]
        return result
