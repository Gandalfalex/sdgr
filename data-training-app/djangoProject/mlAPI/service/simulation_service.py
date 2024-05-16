import numpy as np

from djangoProject.common.default_exceptions.bad_request_exception import BadRequestException
from mlAPI.ml_response_object_classes import SignalDataDTO
from mlAPI.model_training.algorithm_implementation.gap_classifier import GapClassifier
from mlAPI.model_training.model_strategy import get_ml_model
from mlAPI.model_training.run_information import RunInformation
from mlAPI.service.database_service import get_solution_of_config, get_model_configuration
from shared.preprocessing.data_formatting.processing_builder import ProcessingBuilder
from shared.preprocessing.gap_processing import gap_processing as gap
from shared.preprocessing.gap_processing.imputation_algorithm.median_imputation import median_imputation


def load_solution_from_trained_model(user, m_id, pk):
    config = get_model_configuration(pk, m_id, user)
    solution = get_solution_of_config(config)

    train_data = list(config.train_data.all())
    data = [d.time_series_value for d in train_data]
    time_steps = [d.time_stamp_value for d in train_data]

    builder = ProcessingBuilder(config.processing.type.name)
    builder.set_data(data).set_time_stamp_data(time_steps).set_configuration(config.processing.specific_config)

    series_processing, time_processing = builder.get_preprocessors()
    data, pre_config = series_processing.process()
    times, time_config = time_processing.process()

    # if the data contains gaps, override the initial data
    ml_model = get_ml_model(config.ml_model)
    ml_model.set_config(RunInformation(save=solution.generator_model, input_length=len(data[0])))
    gap_classifier = None
    if gap.contains_gaps(times):
        data, times, length = gap.remove_gaps_if_existing(data, times, median_imputation)
        gap_classifier = GapClassifier()
        gap_classifier.set_data(np.array(data))
        gap_classifier.set_config(RunInformation(save=solution.gap_detector_model, input_length=len(data[0])))

    ml_model.set_data(np.array(data))
    result = ml_model.predict_data_from_model()

    if gap_classifier is not None:
        compare_gaps = gap_classifier.mark_gaps(result)
        print(compare_gaps)

    result = series_processing.convert_back(pre_config)
    return SignalDataDTO(config.name, result[0]).get_data()


# Todo change the result, the current state does not support this
def forecast_data_from_trained_model(forecasting_configuration, user, m_id, pk):
    config = get_model_configuration(pk, m_id, user)
    if config.ml_model.forcasting:
        raise BadRequestException("model not for forecasting", "your model has no forcasting capabilities")

    solution = get_solution_of_config(config)

    train_data = list(config.train_data.all())
    data = [d.time_series_value for d in train_data]

    builder = ProcessingBuilder(config.processing.type.name)
    builder.set_data(data).set_configuration(config.processing.specific_config)
    series_processing, _ = builder.get_preprocessors()
    data, pre_config = series_processing.process()
    ml_model = get_ml_model(config.ml_model)
    ml_model.set_config(RunInformation(save=solution.generator_model, input_length=len(data[0])))
    ml_model.set_data(np.array(data))
    length = forecasting_configuration.get("length")
    result = ml_model.forcast(length)
    series_processing.convert_back(pre_config)
    return SignalDataDTO(config.name, result).get_data()
