from shared.response_object_classes import TrainDataFileResponse, TrainDataResponse
from shared.services.database_service import get_all_train_data_files_of_user, get_all_elements_of_file


def get_train_data_files(user):
    files = get_all_train_data_files_of_user(user)
    return [TrainDataFileResponse(i.id, i.name).get_data() for i in files]


def get_train_data_of_file(user, file_id):
    elements = get_all_elements_of_file(file_id, user)
    return [TrainDataResponse(i, length=0).get_data() for i in elements]
