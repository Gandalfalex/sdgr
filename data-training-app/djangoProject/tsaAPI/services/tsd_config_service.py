import logging
import uuid as uid

from djangoProject.common.default_exceptions.not_found_exception import NotFoundException
from djangoProject.common.default_exceptions.unknown_error_exception import UnknownErrorException
from shared.models import TrainData, TrainDataFile
from shared.preprocessing.data_formatting.processing_builder import ProcessingBuilder
from shared.serializer import PreprocessorSerializer, ImputationAlgorithmSerializer
from shared.services.build_processing_service import build_and_manage_processing_configuration
from shared.services.copy_service import create_copy_of_preprocessor, copy_train_data
from shared.services.database_service import get_train_data
from shared.services.training_data_service import get_training_data_by_ids, reduce
from tsaAPI.model_generation.model_types import ModelTypes
from tsaAPI.model_generation.run_information import RunInformation
from tsaAPI.model_generation.tsd_runner import TSDRunner
from tsaAPI.models import TSDConfiguration, TSDModel, TSDConfigurationTrainData
from tsaAPI.serialize_db import TSDConfigurationSerializer
from tsaAPI.services.database_service import get_model_tsd_configuration, get_tsd_model_by_id
from tsaAPI.services.model_strategy import get_tsd_model


class TsdConfigService:

    def get_configs(self, tsd_id, user):
        models = TSDConfiguration.objects.filter(tsd_model_id=tsd_id, user=user).all()
        return [self.__build_config_from_input(model) for model in models]

    def create_config(self, req: {}, tsd_id, user):
        try:
            data = self.__handle_items_and_files(req.get("train_data"), req.get("files"), user)
            model = get_tsd_model_by_id(tsd_id)
            config = TSDConfiguration(tsd_model=model, user=user, name=req.get("name"),
                                      description=req.get("description"))
            config.save()
            config.train_data.set(data)
            config.save()
            return self.__build_config_from_input(config)
        except TSDModel.DoesNotExist as e:
            raise NotFoundException("tsd model does not exist", e.message)

    def update_config(self, tsd_id: int, pk: int, data, user):
        config = get_model_tsd_configuration(pk, tsd_id, user)
        config.name = data["name"]
        config.description = data["description"]
        elements = self.__handle_items_and_files(data["train_data"], data["files"], user)

        config.train_data.set(elements)
        config.save()
        return self.__build_config_from_input(config)

    def get_config(self, tsd_id: int, pk: int, user):
        try:
            config = get_model_tsd_configuration(pk, tsd_id, user)
            return self.__build_config_from_input(config)
        except TSDConfiguration.DoesNotExist as e:
            logging.error("config could not  be found")
            raise NotFoundException("config does not exist", e.message)

    def delete_config(self, tsd_id: int, pk: int, user):
        try:
            config = get_model_tsd_configuration(pk, tsd_id, user)
            TSDConfigurationTrainData.objects.filter(tsd_configuration=config).delete()
            TSDConfiguration.delete(config)
        except TSDConfiguration.DoesNotExist:
            logging.info("tried to remove non existing element")
        return 204

    def get_all_training_data_reduced(self, tsd_id: int, pk: int, user=None):
        config = get_model_tsd_configuration(pk, tsd_id, user)
        data_list = config.train_data.all()
        if data_list is None:
            raise NotFoundException("train data not found or empty", "")
        data = reduce(data_list)
        return data

    def add_preprocessor(self, tsd_id, pk, data, user):
        try:
            config = get_model_tsd_configuration(pk, tsd_id, user)
            config = build_and_manage_processing_configuration(config, data)
            TSDConfiguration.save(config)
            return self.__build_config_from_input(config)
        except Exception as e:
            logging.error(f"{e}")
            return UnknownErrorException("something went wrong", str(e))

    def run_model_setup(self, tsd_id, pk, user):
        try:
            config = get_model_tsd_configuration(pk, tsd_id, user)
            print(f"{config.tsd_model.display_type} is equal to: {config.tsd_model.display_type == 'one_display'}")
            if config.tsd_model.display_type != ModelTypes.ONE_DISPLAY.value:
                converted_data = self.run_model(config)
                for elem in converted_data:
                    try:
                        schema = TSDConfigurationTrainData.objects.get(tsd_configuration=config,
                                                                       train_data_id=elem.get("id")).level_config
                        elem["level_config"] = schema if schema is not None else {}
                    except TSDConfigurationTrainData.DoesNotExist:
                        logging.error("could not find linkage")
                return converted_data
            else:
                return self.run_model(config)
        except Exception as e:
            logging.info(f"{e}")
            raise UnknownErrorException("something went wrong", str(e))

    def run_model_setup_with_custom_body(self, tsd_id: int, pk: int, body: list, user):
        """
        body: [{"trainDataId": 1, "config": {0:1, 1:40, 4: 59}}]
        """

        try:
            config = get_model_tsd_configuration(pk, tsd_id, user)
            data = []
            for i in body:
                m = i.get("trainDataId")
                train_data = config.train_data.filter(id=m).first()
                if train_data is not None:
                    data.append(train_data)

            converted_data = self.run_model(config)
            converted_data = converted_data
            summed_data = [0] * len(converted_data[0]["values"][0].get("data"))
            for i, element in enumerate(converted_data):
                if element.get("id") == body[i].get("trainDataId"):
                    for k, v in body[i].get("config").items():
                        index = int(k)
                        temp = element["values"][index].get("data")
                        temp = temp[v:] + temp[:v]
                        summed_data = [summed_data[x] + temp[x] for x in range(len(summed_data))]

            return [str(x) for x in summed_data]
        except Exception as e:
            logging.info(f"{e}")
            raise UnknownErrorException("something went wrong", str(e))

    def run_model_single_data(self, tsd_id: int, pk: int, td: int, user):
        try:
            config = get_model_tsd_configuration(pk, tsd_id, user)
            train_data = config.train_data.filter(id=td).first()
            schema = TSDConfigurationTrainData.objects.get(tsd_configuration=config,
                                                           train_data_id=td).level_config
            if train_data is not None:
                converted_data = self.run_model(config)[0]
                if len(converted_data) > 0:
                    converted_data["level_config"] = schema
                    return converted_data
            raise NotFoundException("data does not exist", "")
        except Exception as e:
            logging.info(f"{e}")
            raise UnknownErrorException("something went wrong", str(e))

    def run_model(self, config: TSDConfiguration):
        builder = ProcessingBuilder(config.processing.type.name)
        builder.set_min_length(config.min_length)
        builder.set_training_data(list(config.train_data.all()))
        time_steps = [d.time_stamp_value for d in list(config.train_data.all())]
        builder.set_time_stamp_data(time_steps)
        model = get_tsd_model(config.tsd_model)
        runner = TSDRunner()
        task_id = uid.uuid4()
        run_info = RunInformation(uuid=task_id, split=5, display_mode=config.tsd_model.display_type)
        converted_data = runner.run_model(model, builder, run_info)
        return converted_data

    def add_level_config_to_configuration(self, tsd_id: int, pk: int, td: int, user, body):
        config = get_model_tsd_configuration(pk, tsd_id, user)
        train_data = get_train_data(td, user)

        config.level_config = body

        level_config = TSDConfigurationTrainData.objects.get(tsd_configuration=config, train_data=train_data)
        level_config.level_config = body
        level_config.save()

        return self.__build_config_from_input(config)

    def copy_tsd_config(self, tsd_id: int, pk: int, user=None):
        config = get_model_tsd_configuration(pk, tsd_id, user)
        new_name = f"{config.name}_copy"

        model = TSDConfiguration.objects.create(name=new_name, description=config.description,
                                                tsd_model=config.tsd_model, user=user)
        model = create_copy_of_preprocessor(config, model)
        model.save()
        model = copy_train_data(config, model)
        return self.__build_config_from_input(model)

    @staticmethod
    def __build_config_from_input(model: TSDConfiguration):
        serializer = TSDConfigurationSerializer(model)
        if model is None:
            return None
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
        print(items)
        return [get_train_data(i, user) for i in items]