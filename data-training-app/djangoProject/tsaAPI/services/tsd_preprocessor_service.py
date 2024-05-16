import json
import logging

from jsonschema import validate, ValidationError

from shared.models import Preprocessor
from shared.services.database_service import get_preprocessor_type_by_name
from tsaAPI.services.database_service import get_model_tsd_configuration


def add_preprocessor_to_configuration(m_id: int, pk: int, data, user=None):
    """
    the data object should hold the
    :param m_id: ML_model_id
    :param pk: Solution_id
    :param data: json_string of parameters has the form: {"name": PreprocessorType.Name, "data": values}
    :param user: user by jwt
    :return:
    """
    try:
        model_data = get_model_tsd_configuration(pk, m_id, user)
        preprocessor_type = get_preprocessor_type_by_name(data.get("name"))
        try:
            json_data = data.get("data")
            validate(instance=json_data, schema=preprocessor_type.schema)
            preprocessor = Preprocessor(type=preprocessor_type, specific_config=json_data)
            preprocessor.save()
            model_data.processing = preprocessor
            model_data.save()
            return 200, "saved preprocessor to solution"
        except json.JSONDecodeError:
            logging.error("Invalid JSON format.")
        except ValidationError as e:
            logging.error(f"JSON failed validation: {e.message}")
    except Exception as e:
        logging.error(f"{e}")
        return 400, str(e)
