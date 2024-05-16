import logging
from typing import Optional, Any, Tuple, Dict, List

from djangoProject.common.default_exceptions.not_found_exception import NotFoundException
from djangoProject.common.default_exceptions.unknown_error_exception import UnknownErrorException
from mlAPI.models import TrainData, MLConfiguration, MLSolution
from mlAPI.serialize_db import MLConfigurationSerializer
from mlAPI.service.database_service import get_model_configuration, get_model_mlmodel
from shared.models import TrainDataFile
from shared.serializer import PreprocessorSerializer, ImputationAlgorithmSerializer
from shared.services.build_processing_service import build_and_manage_processing_configuration
from shared.services.copy_service import create_copy_of_preprocessor, copy_train_data
from shared.services.database_service import get_train_data
from shared.services.training_data_service import reduce


class SolutionBuilderService:

    def create_configuration(self, req: Dict[str, Any], m_id: int, user: Optional[Any] = None) -> Tuple[int, Any]:
        """
        Create a machine learning solution based on the provided request data.

        :param req: A dictionary containing the request data.
        :param m_id: The ID of the machine learning model.
        :param user: The user associated with the request, if any.
        :return: A tuple containing a status code and either the created solution data or an error message.
        """
        print(f"initial information: {req}")
        try:
            # Retrieve training data based on provided IDs
            data = self.__handle_items_and_files(req.get("train_data"), req.get("files"), user)
            model = get_model_mlmodel(m_id)
            # Create and save the ML configuration
            config = MLConfiguration(
                ml_model=model, user=user,
                name=req.get("name"),
                is_running=None,
                description=req.get("description")
            )
            config.save()
            config.train_data.set(data)
            config.save()

            # Serialize the ML configuration and return it
            return self.__build_config_from_input(config)

        except TrainData.DoesNotExist as e:
            logging.info("Training model not found")
            raise NotFoundException("train data not found", e.message)

    def get_configurations(self, m_id: int, user: Optional[Any] = None) -> List:
        """
        Retrieve all machine learning solutions associated with a specific model and user.

        :param m_id: The ID of the machine learning model.
        :param user: The user associated with the request, if any.
        :return: A tuple containing a status code and either a list of solutions or an error message.
        """

        # Retrieve all ML configurations associated with the given model and user
        model_data = MLConfiguration.objects.filter(ml_model=m_id, user=user)
        data = []

        # Enhance the solution data with additional information
        for i in model_data:
            data.append(self.__build_config_from_input(i))
        return data

    def get_configuration(self, m_id: int, pk: int, user: Optional[Any] = None):
        """
        Retrieve a specific machine learning solution based on its ID, model, and associated user.

        :param m_id: The ID of the machine learning model.
        :param pk: The primary key of the solution.
        :param user: The user associated with the request, if any.
        :return: A tuple containing a status code and either the solution data or an error message.
        """

        # Retrieve the ML configuration based on the provided parameters
        config = get_model_configuration(pk, m_id, user)
        return self.__build_config_from_input(config)

    def update_configuration(self, data: {}, m_id: int, pk: int, user=None):
        temp = get_model_configuration(pk, m_id, user)
        temp.name = data["name"]
        temp.description = data["description"]
        files = self.__handle_items_and_files(data["train_data"], data["files"], user)
        temp.train_data.set(files)
        temp.save()
        return self.__build_config_from_input(temp)

    def get_all_training_data_reduced(self, m_id: int, pk: int, user=None):
        """
        this is a small and simple data reduction algorithm
        :param user: user
        :param m_id: model id
        :param pk: solution id
        :return:
        """
        model = get_model_configuration(pk, m_id, user)
        data_list = model.train_data.all()
        data = reduce(data_list)
        if data_list is None:
            raise NotFoundException("configuration has no training data", "")
        return data

    # TODO add try catch with error message, cannot delete if used anywhere
    def delete_configuration(self, m_id: int, pk: int, user=None):
        model = get_model_configuration(pk, m_id, user)
        MLConfiguration.delete(model)
        return 204

    def add_preprocessor_to_configuration(self, m_id: int, pk: int, data, user=None):
        """
        the data object should hold the
        :param m_id: ML_model_id
        :param pk: Solution_id
        :param data: json_string of parameters has the form: {"name": PreprocessorType.Name, "data": values}
        :param user: user by jwt
        :return:
        """
        try:
            model_data = get_model_configuration(pk, m_id, user)
            model = build_and_manage_processing_configuration(model_data, data)
            MLConfiguration.save(model)
            return self.__build_config_from_input(model)
        except Exception as e:
            logging.error(f"{e}")
            raise UnknownErrorException("something went wrong", str(e))

    def copy_ml_solution(self, m_id: int, pk: int, user=None):
        model_data = get_model_configuration(pk, m_id, user)
        temp = model_data.name + "_copy"

        model = MLConfiguration.objects.create(name=temp, description=model_data.description,
                                               ml_model=model_data.ml_model, user=user)
        model = create_copy_of_preprocessor(model_data, model)
        model.save()
        model = copy_train_data(model_data, model)
        return self.__build_config_from_input(model)

    @staticmethod
    def __build_config_from_input(model: MLConfiguration):
        serializer = MLConfigurationSerializer(model)
        solution = MLSolution.objects.filter(ml_configuration=model).first()
        data = serializer.data

        if model.processing is not None:
            preprocess = PreprocessorSerializer(model.processing)
            data["processing"] = preprocess.data
            data["processing"]["typeName"] = model.processing.type.name
        else:
            data["processing"] = None

        if model.imputation_algorithm is not None:
            imputation_data = ImputationAlgorithmSerializer(model.imputation_algorithm)
            data["imputation_algorithm"] = imputation_data.data
        else:
            data["imputation_algorithm"] = None
        data["solution_id"] = solution.id if solution is not None else 0
        return data

    def __handle_items_and_files(self, items: list, files: list, user):
        for id in files:
            try:
                TrainDataFile.objects.get(pk=id)
                items_from_file = TrainData.objects.filter(file_id=id).all()
                [items.append(i.id) for i in items_from_file]
            except NotFoundException as e:
                raise NotFoundException("element not found", e)
            except Exception as e:
                raise UnknownErrorException("not found", str(e))
        items = list(set(items))
        return [get_train_data(i, user) for i in items]
