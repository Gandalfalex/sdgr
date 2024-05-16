import logging

from django.db import connection, IntegrityError

from djangoProject.common.default_exceptions.not_found_exception import NotFoundException
from djangoProject.common.default_exceptions.unique_constraint_violation_exception import \
    UniqueConstraintViolationException
from shared.models import PreprocessorType, TrainData, ImputationAlgorithm, TrainDataFile


def get_preprocessor_type_by_name(name: str) -> PreprocessorType:
    try:
        return PreprocessorType.objects.get(name=name)
    except PreprocessorType.DoesNotExist as e:
        logging.error("name of preprocessor not found")
        raise NotFoundException("name of preprocessor not found", e)


def get_preprocessor_type_by_id(pk: int) -> PreprocessorType:
    try:
        return PreprocessorType.objects.get(pk=pk)
    except PreprocessorType.DoesNotExist as e:
        logging.error("preprocessor does not exist")
        raise NotFoundException("preprocessor does not exist", e)


def get_train_data(pk: int, user) -> TrainData:
    try:
        return TrainData.objects.get(pk=pk, user=user)
    except TrainData.DoesNotExist as e:
        logging.error("TrainData does not exist")
        raise NotFoundException("train data does not exist", e)


def get_preprocessor_by_name(name: str):
    try:
        return PreprocessorType.objects.get(name=name)
    except PreprocessorType.DoesNotExist as e:
        logging.error("PreprocessorType does not exist")
        raise NotFoundException("PreprocessorType data does not exist", e)


def get_imputation_algorithm_by_name(name: str):
    try:
        return ImputationAlgorithm.objects.get(name=name)
    except ImputationAlgorithm.DoesNotExist as e:
        logging.error(f"ImputationAlgorithm not found by name: {name}")
        raise NotFoundException("PreprocessorType data does not exist", e)


def get_train_data_file(pk, u_id):
    try:
        return TrainDataFile.objects.get(pk=pk, user_id=u_id)
    except TrainDataFile.DoesNotExist as e:
        logging.error(f"TrainDataFile not found")
        raise NotFoundException("TrainDataFile data does not exist", e)


def get_all_train_data_files_of_user(user):
    try:
        return TrainDataFile.objects.filter(user=user).all()
    except Exception as e:
        raise NotFoundException("no TrainDataFile found", e)

def get_all_elements_of_file(file_id, user):
    try:
        file = TrainDataFile.objects.get(pk=file_id, user=user)
        return TrainData.objects.filter(user=user, file=file).all()
    except TrainDataFile.DoesNotExist as e:
        raise NotFoundException("file does not exist", e)


def check_file_usage_before_deletion(file_id, user):
    query = ("SELECT COUNT(td) " +
             "FROM train_data td " +
             "WHERE td.file_id = %s " +
             "AND td.user_id = %s "
             "AND NOT EXISTS ( SELECT 1 FROM ml_configuration_train_data mctd WHERE mctd.traindata_id = td.id ) " +
             "AND NOT EXISTS ( SELECT 1 FROM tsd_configuration_train_data tctd WHERE tctd.train_data_id = td.id ) ")
    with connection.cursor() as cursor:
        cursor.execute(query, [file_id, user.id])
        row = cursor.fetchone()
        return row[0] if row else 0

def delete_all_elements_of_file(file_id, user):
    query = ("DELETE " +
             "FROM train_data td " +
             "WHERE td.file_id = %s " +
             "AND td.user_id = %s "
             "AND NOT EXISTS ( SELECT 1 FROM ml_configuration_train_data mctd WHERE mctd.traindata_id = td.id ) " +
             "AND NOT EXISTS ( SELECT 1 FROM tsd_configuration_train_data tctd WHERE tctd.train_data_id = td.id ) ")
    with connection.cursor() as cursor:
        cursor.execute(query, [file_id, user.id])




def get_or_create_train_data_file(name, user):
    try:
        return TrainDataFile.objects.get(name=name, user=user)
    except TrainDataFile.DoesNotExist:
        try:
            file = TrainDataFile(name=name, user=user)
            file.save()
            return file
        except IntegrityError:
            raise UniqueConstraintViolationException("name of file has to be unique",
                                                     "provide a new name or use old file")


def get_ml_config_count(pk, u_id):
    query = ("SELECT COUNT(td.id) FROM train_data td "
             "JOIN ml_configuration_train_data mctd ON mctd.traindata_id = td.id "
             "WHERE td.id = %s AND td.user_id = %s")
    with connection.cursor() as cursor:
        cursor.execute(query, [pk, u_id])
        row = cursor.fetchone()
        return row[0] if row else 0


def get_tsd_config_count(pk, u_id):
    query = ("SELECT COUNT(td.id) FROM train_data td "
             "JOIN tsd_configuration_train_data tctd ON tctd.train_data_id = td.id "
             "WHERE td.id = %s AND td.user_id = %s")
    with connection.cursor() as cursor:
        cursor.execute(query, [pk, u_id])
        row = cursor.fetchone()
        return row[0] if row else 0


def can_delete(pk, u_id):
    query = ("SELECT COUNT(td.id) FROM train_data td "
             "JOIN tsd_configuration_train_data tctd ON tctd.train_data_id = td.id "
             "JOIN ml_configuration_train_data mctd ON mctd.traindata_id = td.id "
             "WHERE td.id = %s AND td.user_id = %s")
    with connection.cursor() as cursor:
        cursor.execute(query, [pk, u_id])
        row = cursor.fetchone()
        return False if row[0] != 0 else True
