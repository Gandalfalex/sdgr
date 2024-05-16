import numpy as np
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM, RepeatVector, Permute, Multiply
from keras.models import Model
from numpy import random

from models_for_testing.ml_model_general import GeneralMLModel

np.random.seed(1337)


class RNN_NOTWORKING(GeneralMLModel):
    max_features = 5883
    batch_size = 32
    in_out_neurons = 2
    hidden_neurons = 300

    def _load_data(self, data, n_prev=10):
        docx, docy = [], []
        for i in range(len(data) - n_prev):
            docx.append(data[i:i + n_prev])
            docy.append(data[i + n_prev])

        all_x = np.array(docx)
        all_y = np.array(docy)
        return all_x, all_y

    def train_test_split(self, data, test_size=0.2):
        ntrn = round(len(data) * (1 - test_size))
        x_train, y_train = self._load_data(data[0:ntrn])
        x_test, y_test = self._load_data(data[ntrn:])
        return (x_train, y_train), (x_test, y_test)

    def rnn_lstm(self, test_size=0.2):
        input_dim = 32
        hidden = 32
        step = 1

        print('Loading data...')
        test_element = self.data[random.randint(0, len(self.data))]
        (x_train, y_train), (x_test, y_test) = self.train_test_split(test_element, test_size)

        x_train = sequence.pad_sequences(x_train, maxlen=self.run_information.get("input_length"))
        x_test = sequence.pad_sequences(x_test, maxlen=self.run_information.get("input_length"))

        model1 = Sequential()
        model1.add(LSTM(units=hidden, input_shape=(self.run_information.get("input_length"), ), return_sequences=True))

        model2 = Sequential()
        model2.add(Dense(units=step, input_dim=input_dim))
        model2.add(Activation('softmax'))
        model2.add(RepeatVector(hidden))
        model2.add(Permute((2, 1)))

        merged_output = Multiply()([model1.output, model2.output])
        merged_output = LSTM(1)(merged_output)

        model = Model([model1.input, model2.input], merged_output)
        model.compile(loss='mse', optimizer='sgd')
        x = np.array([x_train, x_train])
        print(x.shape)
        model.fit([x_train, x_train, x_train], y_train, batch_size=self.batch_size, validation_data=([x_test, x_test], y_test),
                  epochs=5)
        score = model.evaluate([x_test, x_test], y_test, batch_size=self.batch_size)
        model.save("saved_models/{}.keras".format(self.run_information.get("uuid")))
        return score

    def run(self):
        print(self.rnn_lstm(0.5))
