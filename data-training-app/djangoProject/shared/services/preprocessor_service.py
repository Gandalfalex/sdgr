import copy
import json

from mlAPI.service.database_service import get_model_configuration
from shared.models import Preprocessor, PreprocessorType, SchemaValidationForms, ImputationAlgorithm
from shared.serializer import PreprocessorTypeSerializer, PreprocessorSerializer
from shared.services.database_service import get_preprocessor_type_by_id
from tsaAPI.services.database_service import get_model_tsd_configuration


def get_preprocessor(pk):
    try:
        data = Preprocessor.objects.get(pk=pk)
        serializer = PreprocessorSerializer(data)
        return serializer.data
    except Preprocessor.DoesNotExist:
        return None


def get_all_preprocessor_types():
    # TODO convert dict to json
    schema = build_schema()
    return schema


def get_preprocessor_type(pk):
    data = get_preprocessor_type_by_id(pk)
    serializer = PreprocessorTypeSerializer(data)
    return serializer.data


def get_preprocessor_for_from_ml(m_id, pk, user):
    try:
        model = get_model_configuration(pk, m_id, user)
        data = model.processing
        serializer = PreprocessorSerializer(data)
        return serializer.data
    except Preprocessor.DoesNotExist:
        return 200, "Preprocessor not found"


def get_preprocessor_for_from_tsd(tsd_id, pk, user):
    try:
        model = get_model_tsd_configuration(pk, tsd_id, user)
        data = model.processing
        serializer = PreprocessorSerializer(data)
        return serializer.data
    except Preprocessor.DoesNotExist:
        return 200, "Preprocessor not found"


def build_schema():
    processor_options = PreprocessorType.objects.all()
    main_schema = SchemaValidationForms.objects.get(name="default_validation_schema")
    validation_form = SchemaValidationForms.objects.get(name="customization_option")
    options = {k.name: k.schema for k in processor_options}
    imputation_algorithm = ImputationAlgorithm.objects.all()
    processing = "Processor Type"
    imputation = "Imputation_Algorithm"
    data = __build_enum_from_main_key(main_schema.schema, processing,
                                      description="select your processing option, could improve training result and "
                                                  "time")
    data = __fill_enums(data, processing, [m for m in options])

    data = __build_enum_from_main_key(data, imputation, description="select an algorithm to fill in your gaps")
    data = __fill_enums(data, imputation, [s.name for s in imputation_algorithm])

    build_dependency_data = [__create_if_then_else_schema(validation_form.schema, processing, name, value) for name, value in
                             options.items()]
    data = __fill_dependencies(data, processing, build_dependency_data)
    ui_option = validation_form.ui_schema
    ui_option.update(main_schema.ui_schema)
    ui_option.update(__build_ui_option_for_enum(processing))
    ui_option.update(__build_ui_option_for_enum(imputation))
    return {"schema": data, "ui_schema": ui_option}


def __build_enum_from_main_key(original_data: {}, key: str, json_type="string", description=""):
    original_data["properties"][key] = {"type": json_type, "enum": [], "description": description}
    original_data["required"].append(key)
    return original_data


def __fill_enums(original_data: {}, key: str, values: []):
    original_data["properties"][key]["enum"] = values
    return original_data


def __fill_dependencies(original_data, key, dependency_data: []):
    original_data["dependencies"] = {key: {"oneOf": dependency_data}}
    return original_data


def __build_ui_option_for_enum(key):
    return {key: {
        "ui:widget": "radio",
        "ui:options": {
            "inline": True
        },
        "ui:placeholder": "Choose an option"
    }}


def __create_if_then_else_schema(schema_original: {}, key: str, key_name: str, then_part: {}):
    easy_read_then_part = {"properties": {
        f"{key_name}Option": then_part
    }}

    schema = copy.deepcopy(schema_original)
    schema["properties"][key] = {"const": key_name}
    schema["then"] = easy_read_then_part
    schema["else"] = {
        "properties": {
            key_name: {
                "type": "object",
                "additionalProperties": False
            }
        }
    }
    return schema
