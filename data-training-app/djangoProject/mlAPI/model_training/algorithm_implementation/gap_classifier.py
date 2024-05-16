import numpy as np
from keras import Sequential
from keras.src.layers import Dense
from sklearn.model_selection import train_test_split

from mlAPI.model_training.ml_model_general import GeneralMLModel


class GapClassifier(GeneralMLModel):

    def build_model(self, length):
        model = Sequential()
        model.add(Dense(length, activation='relu', input_shape=(length,)))
        model.add(Dense(length, activation='relu'))
        model.add(Dense(length, activation='sigmoid'))

        model.compile(optimizer='adam',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])
        return model

    def run(self):
        print(f"gap detection input length = {self.run_information.get_input_length()}")
        x = self.data
        y = self.data
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        model = self.build_model(len(self.data[0]))
        model.fit(np.array(x_train), np.array(y_train), epochs=200, batch_size=1, validation_split=0.1, verbose=0)
        self.save(model)
        return self.run_information

    def mark_gaps(self, prediction_data):
        model = self.load_model()
        return model.predict(np.array([prediction_data]))
