from django.db import models
from mlAPI.models import TrainData
from shared.models import Preprocessor, JwtUser, ImputationAlgorithm
from tsaAPI.model_generation.model_types import ModelTypes


class TSDModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, help_text="name representation for the frontend")
    i18n_key = models.CharField(max_length=30, help_text="translation key for the description")
    description = models.CharField(max_length=255, help_text="description of the model for the frontend")
    pyName = models.CharField(max_length=50, help_text="name of the python file that represents the model")
    display_type = models.CharField(max_length=50, choices=[(choice.name, choice.value) for choice in ModelTypes],
                                    help_text="different display types for the model", default=ModelTypes.SPLITTING)
    created_at = models.DateTimeField(auto_now_add=True, help_text="created at")

    class Meta:
        db_table = 'tsd_models'


class TSDTrainingInformation(models.Model):
    id = models.AutoField(primary_key=True)
    tsd_configuration = models.ForeignKey('TSDConfiguration', on_delete=models.CASCADE)
    added_to = models.DateTimeField(auto_now_add=True, help_text="time it was added")
    accuracy = models.FloatField(help_text="accuracy achieved")
    levels = models.IntegerField(help_text="levels of separation")

    class Meta:
        db_table = 'tsd_training_information'


class TSDConfiguration(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(JwtUser, on_delete=models.CASCADE, help_text='User who owns this solution builder')
    name = models.CharField(max_length=255, help_text="name representation for the frontend")
    description = models.CharField(max_length=500, help_text='description of the model for the frontend', null=True)
    processing = models.OneToOneField(Preprocessor, help_text='preprocessing to speed up training', null=True,
                                      on_delete=models.CASCADE)
    tsd_model = models.ForeignKey(TSDModel, on_delete=models.CASCADE)
    train_data = models.ManyToManyField(TrainData, through='TSDConfigurationTrainData',
                                        help_text='n:m, training data for the model')
    created_at = models.DateTimeField(auto_now_add=True)
    imputation_algorithm = models.ForeignKey(ImputationAlgorithm, help_text='algorithm used to impute data',
                                             on_delete=models.SET_NULL, null=True)
    min_length = models.IntegerField(help_text="reduction value to which every dataset is trimmed before training",
                                     null=True)

    class Meta:
        db_table = 'tsd_configuration'


class TSDConfigurationTrainData(models.Model):
    tsd_configuration = models.ForeignKey(TSDConfiguration, on_delete=models.CASCADE)
    train_data = models.ForeignKey(TrainData, on_delete=models.CASCADE)
    level_config = models.JSONField(help_text='configuration for level', null=True)

    class Meta:
        db_table = 'tsd_configuration_train_data'
