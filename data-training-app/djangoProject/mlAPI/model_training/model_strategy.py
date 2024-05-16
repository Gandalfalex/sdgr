from mlAPI.model_training.algorithm_implementation.cgan import CGAN
from mlAPI.model_training.algorithm_implementation.gan import GAN
from mlAPI.model_training.algorithm_implementation.lstm import LSTMCustom
from mlAPI.model_training.algorithm_implementation.rnn import RNN
from mlAPI.models import MLModel


def get_ml_model(model: MLModel):
    print(model.pyName)
    match model.pyName:
        case "GAN.py":
            return GAN()
        case "RNN.py":
            return RNN()
        case "LSTM.py":
            return LSTMCustom()
        case "CGAN.py":
            return CGAN()
        case None:
            return None
