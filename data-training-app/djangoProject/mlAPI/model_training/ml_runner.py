import logging
from concurrent.futures import ProcessPoolExecutor
from typing import Any

import numpy as np
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from mlAPI.model_training.algorithm_implementation.gap_classifier import GapClassifier
from mlAPI.model_training.run_information import RunInformation
from mlAPI.models import MLConfiguration, MLSolution, MLTrainingInformation
from shared.models import Preprocessor
from shared.preprocessing.data_formatting.processing_builder import ProcessingBuilder
from shared.preprocessing.gap_processing import gap_processing as gap
from shared.preprocessing.gap_processing.imputation_algorithm.median_imputation import median_imputation
from shared.services.database_service import get_preprocessor_type_by_name


class MlRunner:
    """
    A class to run machine learning models with support for gap detection and handling.

    Attributes:
        channel_layer: The channel layer used for asynchronous communication.
        executor: A process pool executor for running tasks in parallel.
        data: A list of numpy arrays containing the training data.
        time_steps: A list of numpy arrays containing the time steps corresponding to the training data.
        tasks: A dictionary to store the futures of running tasks.
    """

    channel_layer = get_channel_layer()
    executor = ProcessPoolExecutor(max_workers=10)
    data = []
    time_steps = []

    tasks = {}

    def run_model(self, model: Any, builder: ProcessingBuilder, config: RunInformation) -> str:
        """
        Runs the machine learning model.

        Args:
            model: The machine learning model to be run.
            builder: The preprocessorBuilder to be used on the data.
            config: A dictionary containing the configuration for the model.

        Returns:
            A string representing the UUID of the running task.:
        """
        series_processing, time_processing = builder.get_preprocessors()
        data, pre_process_config = series_processing.process()
        time_steps, _ = time_processing.process()
        config.input_length = series_processing.min_length
        if gap.contains_gaps(self.time_steps):
            config.gaps = True
            data, time, length = gap.remove_gaps_if_existing(data, time_steps, median_imputation)

            config.input_length = length
            config.is_running_gaps = True
            self.__run_future(self.__gap_classifier_callback, GapClassifier(), np.array(time), config,
                              "gap_detection_{}".format(config.get_uuid()))

        try:
            preprocessing_type = get_preprocessor_type_by_name(series_processing.name)
            preprocessor_config = Preprocessor(type=preprocessing_type, specific_config=pre_process_config)
            preprocessor_config.save()
        except Exception as e:
            logging.error(f"could save preprocessor: {e}")

        # TODO change that, only required for gan currently i think
        data = data + data
        config.is_running_gaps = False

        temp = self.__run_future(self.__generator_callback, model, np.array(data), config, config.get_uuid())
        return temp

    def __run_future(self, callback: Any, model: Any, data: np.ndarray, config: RunInformation, task_key: str) -> str:
        """
        Runs a future task.

        Args:
            callback: The callback function to be called when the task is finished.
            model: The machine learning model to be run.
            data: The training data as a numpy array.
            config: A dictionary containing the configuration for the model.
            task_key: A string representing the key to store the future in the task's dictionary.

        Returns:
            A string representing the UUID of the running task.
        """
        model.set_data(data)
        model.set_config(config)
        future = self.executor.submit(model.run)
        future.add_done_callback(callback)
        self.tasks[task_key] = future
        return config.get_uuid()

    def __generator_callback(self, future: Any) -> None:
        """
        Callback function for when the generator model training is finished.

        Args:
            future: The future object representing the running task.
        """

        result = future.result()
        status = {"status": "finished"}
        async_to_sync(self.channel_layer.group_send)(result.identifier,
                                                     {"type": "chat_message", "message": status})
        self.tasks.pop(result.get_uuid())

        try:
            model = MLConfiguration.objects.get(pk=result.configuration_id)
            model.is_running = None
            model.save()
            try:
                solution = MLSolution.objects.get(ml_configuration=model)
                solution.generator_model = result.get_save()
                solution.save()
                try:
                    old = MLTrainingInformation.objects.get(ml_solution=solution)
                    MLTrainingInformation.delete(old)
                except MLTrainingInformation.DoesNotExist:
                    logging.info("failed to delete old Training Information")
            except MLSolution.DoesNotExist:
                solution = MLSolution(ml_configuration=model)
                solution.generator_model = result.get_save()
                solution.save()
            logging.info("calling to save train Information")
            self.__save_train_information(result, solution)
        except MLConfiguration.DoesNotExist:
            logging.info("solution not found")

    def __save_train_information(self, data: RunInformation, model: MLSolution) -> None:
        """
        Saves the training information.

        Args:
            data: A dictionary containing the training information.
            model: The MLSolution object to save the training information to.
        """
        info = MLTrainingInformation(ml_solution=model)
        info.ml_solution = model
        info.training_time = data.runtime
        info.iterations = data.get_iterations()

        info.max_length = data.get_input_length()
        info.image = data.image
        async_to_sync(self.channel_layer.group_send)(data.identifier,
                                                     {"type": "chat_disconnect", "message": {"status": "closing"}})
        try:
            info.save()
        except Exception as e:
            logging.error(f"Error saving info: {e}")

    def __gap_classifier_callback(self, future: Any) -> None:
        """
        Callback function for when the gap classifier model training is finished.

        Args:
            future: The future object representing the running task.
        """
        result = future.result()
        status = {"status": "finished classifier"}
        async_to_sync(self.channel_layer.group_send)(result.identifier,
                                                     {"type": "chat_message", "message": status})

        self.tasks.pop("gap_detection_{}".format(result.get_uuid))
        try:
            model = MLConfiguration.objects.get(pk=result.configuration_id)
            try:
                solution = MLSolution.objects.get(ml_configuration_id=model)
                solution.gap_detector_model = result.get_save()
                solution.save()
            except MLSolution.DoesNotExist:
                solution = MLSolution(ml_configuration=model)
                solution.gap_detector_model = result.get_save
                solution.save()
            logging.info("calling to save train Information")
        except MLConfiguration.DoesNotExist:
            logging.info("solution not found")
