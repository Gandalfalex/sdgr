from keras.callbacks import Callback
from mlAPI.websocket_callbacks.base_callback import MLCallback


class KerasCallback(Callback):
    callback = None

    def __init__(self, run_information):
        super().__init__()
        self.callback = MLCallback(run_information)

    def on_epoch_end(self, epoch, logs=None):
        self.callback.send_progress(epoch)
