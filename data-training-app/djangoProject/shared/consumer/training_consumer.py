import logging
import uuid as uid

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from djangoProject.common.default_exceptions.unknown_error_exception import UnknownErrorException
from mlAPI.model_training.ml_runner import MlRunner
from mlAPI.model_training.model_strategy import get_ml_model
from mlAPI.model_training.run_information import RunInformation
from mlAPI.models import MLConfiguration
from shared.preprocessing.data_formatting.processing_builder import ProcessingBuilder


class StatusConsumer(JsonWebsocketConsumer):
    # keep track of current runs
    runners = {}

    def connect(self):
        group_name = f"model{self.scope['ml_id']}solution{self.scope['sol_id']}"
        try:
            async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)
            self.scope["group"] = group_name
            self.accept()
        except Exception as e:
            logging.error(e)
            raise UnknownErrorException("cannot connect", reason=str(e))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.scope["group"], self.channel_name)

    def receive_json(self, message, **kwargs):
        response = self.prepare_data(message)
        self.send_json(response)

    def chat_message(self, event):
        self.send_json(event["message"])

    def chat_disconnect(self, event):
        self.send_json(event["message"])
        self.close()
        self.runners.get(event["uuid"])

    def prepare_data(self, message):
        task_id = uid.uuid4()
        try:
            iterations = message.get("iterations")
            model = MLConfiguration.objects.get(ml_model_id=self.scope["ml_id"], pk=self.scope["sol_id"])
        except MLConfiguration.DoesNotExist:

            return self.disconnect("ml_model does not exist")
        if model.is_running is not None:
            return {"status": "already running"}

        # Define a way to customize the preprocessor and make it part of Configuration
        data = [d.time_series_value for d in list(model.train_data.all())]
        time_steps = [d.time_stamp_value for d in list(model.train_data.all())]
        builder = ProcessingBuilder(model.processing.type.name)
        builder.set_min_length(model.min_length)
        builder.set_data(data)
        builder.set_time_stamp_data(time_steps)
        print("builder is set")
        ml_model = get_ml_model(model.ml_model)

        runner = MlRunner()
        run_info = RunInformation(iterations=iterations, uuid=task_id, configuration_id=model.id,
                                  identifier=self.scope["group"])
        try:
            runner.run_model(ml_model, builder, run_info)
            model.is_running = task_id
            MLConfiguration.save(model)
        except Exception as e:
            print(f"{e}")
        logging.info("start running")

        response = {"message": "start sending"}
        return response
