from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from mlAPI.model_training.run_information import RunInformation


class MLCallback:
    """
    This is the base class for callbacks, either inherit from it or import it.
    """
    channel_layer = get_channel_layer()
    run_information = RunInformation()

    def __init__(self, run_information: RunInformation):
        self.run_information = run_information

    def send_progress(self, epoch):
        message = {"type": "django",
                   "progress": self.run_information.get_progress(epoch),
                   "message": "running element"}
        async_to_sync(self.channel_layer.group_send)(self.run_information.identifier,
                                                     {"type": "chat_message", "message": message})
