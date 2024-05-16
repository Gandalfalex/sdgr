from typing import List

from shared.preprocessing.data_formatting.default_processing import DefaultPreprocessing
from shared.preprocessing.data_formatting.preprocess import PreProcessing
from shared.services.database_service import get_preprocessor_by_name
from shared.strategies.preprocessing_strategy import get_preprocessor_strategy


class ProcessingBuilder:
    processor: PreProcessing = None
    name = ""
    default_processor = DefaultPreprocessing()
    train_id_list: List

    def __init__(self, name: str):
        self.name = name
        preprocessor_type = get_preprocessor_by_name(name)
        preprocess_imp = get_preprocessor_strategy(preprocessor_type)
        self.processor = preprocess_imp

    def set_min_length(self, min_length: int):
        self.processor.min_length = min_length
        self.default_processor.min_length = min_length
        return self

    def set_data(self, data: []):
        self.processor.set_data(data)
        return self

    def set_training_data(self, data: []):
        values = []
        train_data_ids = []
        for i in data:
            temp = {"id": i.id, "name": i.name}
            (train_data_ids.append(temp))
            values.append(i.time_series_value)
        self.train_id_list = train_data_ids
        self.processor.set_data(values)

    def set_time_stamp_data(self, data: []):
        self.default_processor.set_data(data)
        return self

    def set_configuration(self, configuration: {}):
        self.processor.set_config(configuration)
        return self

    def get_preprocessors(self):
        """
        :return: return both preprocessors, the first is customized specifically for time series data, the second is
        default to also process the time stamps accordingly
        """
        return self.processor, self.default_processor
