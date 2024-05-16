import base64
import io

import h5py
from keras import models, Sequential
from keras.src.layers import Dense
from keras.src.saving.saving_api import load_model

from models_for_testing.ml_model_general import GeneralMLModel
import numpy as np
from sklearn.model_selection import train_test_split


class Gap_classifier(GeneralMLModel):

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
        x = self.data
        y = self.data
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        model = self.build_model(len(self.data[0]))
        model.fit(np.array(x_train), np.array(y_train), epochs=20, batch_size=1, validation_split=0.1)
        buffer = io.BytesIO()
        with h5py.File(buffer, 'w') as f:
            model.save(f)

        # model.save(buffer, save_format="h5")
        model_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        self.run_information["save"] = model_base64
        return self.run_information

    def get_gaps(self, sampleData):
        buffer = io.BytesIO(base64.b64decode(self.run_information.get("save")))
        model = None
        with h5py.File(buffer, 'r') as f:
            model = load_model(f)
        temp = model.predict(np.array([sampleData]))
        return temp
