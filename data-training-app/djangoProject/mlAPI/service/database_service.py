import logging

from djangoProject.common.default_exceptions.not_found_exception import NotFoundException
from mlAPI.models import MLConfiguration, MLModel, MLSolution


def get_model_configuration(pk: int, ml_model_id: int, user=None):
    try:
        return MLConfiguration.objects.get(ml_model_id=ml_model_id, pk=pk, user=user)
    except MLConfiguration.DoesNotExist as e:
        logging.error(f"configuration not found {e}")
        raise NotFoundException("configuration could not be found", e)


def get_model_mlmodel(pk: int) -> MLModel:
    try:
        return MLModel.objects.get(pk=pk)
    except MLModel.DoesNotExist as e:
        raise NotFoundException("mlmodel does not exist", e)


def get_solution_of_config(config: MLConfiguration) -> MLSolution:
    try:
        return MLSolution.objects.get(ml_configuration=config)
    except MLSolution.DoesNotExist as e:
        raise NotFoundException("ml solution does not exist", e)
