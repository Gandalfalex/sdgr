import numpy as np

from shared.preprocessing.data_formatting.processing_builder import ProcessingBuilder
from tsaAPI.model_generation.algorithms.tsd_model_general import GeneralTSDModel
from tsaAPI.model_generation.model_types import ModelTypes
from tsaAPI.model_generation.run_information import RunInformation
from tsaAPI.response_object_classes import TSAValueElement


class TSDRunner:

    def __init__(self):
        self.model = None
        self.preprocessor = None

    def run_model(self, model: GeneralTSDModel, builder: ProcessingBuilder, config: RunInformation):
        series_processing, time_processing = builder.get_preprocessors()
        information = builder.train_id_list

        y_data, pre_process_config = series_processing.process()
        x_data, _ = time_processing.process()

        config.input_length = series_processing.min_length
        values = []
        print(config.display_mode == ModelTypes.ONE_DISPLAY.value)
        if config.display_mode == ModelTypes.ONE_DISPLAY.value:
            model.set_data(y_data)
            model.set_x_values(x_data)
            model.set_config(config)
            _, result = model.run()

            element = TSAValueElement(element_id=3, name="asd", values=result, levels=len(result),
                                      element_type=config.display_mode)
            return [element.get_data()]

        for i in zip(information, y_data, x_data):
            array = np.array(i[1])
            model.set_data(array)
            model.set_x_values(np.array(i[2]))
            model.set_config(config)
            _, result = model.run()
            element = TSAValueElement(i[0].get("id"), i[0].get("name"), result, len(result), "normal")
            values.append(element.get_data())
        return values
