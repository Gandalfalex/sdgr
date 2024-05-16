import base64
import logging
from io import BytesIO
from typing import List

from keras.src import Model
import numpy as np
from keras.src.saving.saving_api import load_model
from matplotlib import pyplot as plt

from mlAPI.model_training.run_information import RunInformation


class GeneralMLModel:
    data: List[np.ndarray] = None
    run_information: RunInformation = None

    def set_config(self, config: RunInformation):
        self.run_information = config

    def set_data(self, data: List[np.ndarray]):
        """Set the data attribute of the object.

        :param data: The data to be set.
        :return: None
        """
        self.data = data

    def run(self):
        """
        start running the training
        :param uuid: uuid represents the name,
        :param ml_solution_id: solution id of the configuration
        :return: self.run_information
        """
        pass

    def predict_data_from_model(self):
        """
        get a prediction or rework of the data
        :param data:
        :return:
        """
        pass

    def forcast(self, limit: int, starting_point: int = -1) -> []:
        pass

    def save(self, model: Model) -> RunInformation:
        model.save("saved_models/{}.keras".format("value"))
        with open("saved_models/{}.keras".format("value"), 'rb') as model_file:
            model_base64 = base64.b64encode(model_file.read()).decode('utf-8')
        self.run_information.save_model(model_base64)
        return self.run_information

    def load_model(self) -> Model:
        model_base64 = self.run_information.get_save()
        with open("saved_models/{}.keras".format("value"), 'wb') as model_file:
            model_file.write(base64.b64decode(model_base64))
        model = load_model("saved_models/{}.keras".format("value"), compile=False)
        return model

    def create_image(self, real: List[np.array], synthetic: List[np.array], title: str):
        try:
            plt.title(title)
            plt.plot(real, label="real data")
            plt.plot(synthetic, label="synthetic data")
            plt.legend()
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()

            base64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            self.run_information.image = base64_str
        except Exception as e:
            logging.error(e)
