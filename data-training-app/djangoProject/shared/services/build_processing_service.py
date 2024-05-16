import json
import logging

from djangoProject.common.default_exceptions.bad_request_exception import BadRequestException
from shared.models import Preprocessor
from shared.services.database_service import get_preprocessor_type_by_name, get_imputation_algorithm_by_name


def build_and_manage_processing_configuration(model_data, data: {}):
    try:
        preprocessing_algo = data.get("Processor Type")
        preprocessor_type = get_preprocessor_type_by_name(preprocessing_algo)
        imputation_algo = get_imputation_algorithm_by_name(data.get("Imputation_Algorithm"))
        try:
            json_data = data.get(f"{preprocessing_algo}Option", {})
            model_data.imputation_algorithm = imputation_algo
            preprocessor = Preprocessor(type=preprocessor_type, specific_config=json_data)
            preprocessor.save()
            print("processing saved")
            model_data.processing = preprocessor
            model_data.min_length = data.get("min_length")
            print(data.get("min_length"))
            return model_data
        except json.JSONDecodeError as jex:
            logging.error("Invalid JSON format.")
            raise BadRequestException("invalid json_format", reason=jex)
    except Exception as e:
        logging.error(e)
    return None
