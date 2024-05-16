import logging

from djangoProject.common.default_exceptions.not_found_exception import NotFoundException
from tsaAPI.models import TSDConfiguration, TSDModel


def get_model_tsd_configuration(pk: int, model_id: int, user=None) -> TSDConfiguration:
    try:
        return TSDConfiguration.objects.get(tsd_model_id=model_id, user=user, pk=pk)
    except TSDConfiguration.DoesNotExist as e:
        logging.error("configuration does not exist")
        raise NotFoundException("configuration does not exist", e)


def get_tsd_model_by_id(pk: int) -> TSDModel:
    try:
        return TSDModel.objects.get(pk=pk)
    except TSDModel.DoesNotExist as e:
        logging.error("configuration does not exist")
        raise NotFoundException("model does not exist", e)
