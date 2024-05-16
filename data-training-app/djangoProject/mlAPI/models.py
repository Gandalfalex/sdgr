from django.contrib.auth.models import User
from django.db import models

from shared.models import TrainData, JwtUser, Preprocessor, ImputationAlgorithm


class MLModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, help_text='name representation for the frontend')
    description = models.CharField(max_length=255, help_text='description of the model for the frontend')
    i18n_key = models.CharField(max_length=50, help_text="translation key for the description")
    pyName = models.CharField(max_length=255, help_text='name of the python file that represents the model')
    created_at = models.DateTimeField(auto_now_add=True, help_text='created at')
    forcasting = models.BooleanField(default=False, help_text="Not every model has forcast capabilities")

    class Meta:
        db_table = 'ml_model'


class MLConfiguration(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(JwtUser, on_delete=models.CASCADE, help_text='User who owns this solution builder')
    name = models.CharField(max_length=50, help_text='name representation for the frontend')
    description = models.CharField(max_length=500, help_text='description of the model for the frontend', null=True)
    processing = models.OneToOneField(Preprocessor, help_text='preprocessing to speed up training', null=True,
                                      on_delete=models.CASCADE)
    ml_model = models.ForeignKey(MLModel, on_delete=models.CASCADE, help_text='model used for this configuration')
    train_data = models.ManyToManyField(TrainData, help_text='n:m, training data for the model')
    created_at = models.DateTimeField(auto_now_add=True)
    is_running = models.CharField(max_length=50, help_text="if uuid = null, not running", null=True)
    imputation_algorithm = models.ForeignKey(ImputationAlgorithm, help_text='algorithm used to impute data',
                                             on_delete=models.SET_NULL, null=True)
    min_length = models.IntegerField(help_text="reduction value to which every dataset is trimmed before training",
                                     null=True)

    class Meta:
        db_table = 'ml_configuration'


class MLSolution(models.Model):
    id = models.AutoField(primary_key=True)
    ml_configuration = models.OneToOneField(MLConfiguration, on_delete=models.CASCADE,
                                            help_text='id of the solution-builder')
    generator_model = models.TextField(help_text="base64 decoded keras model", null=False)
    gap_detector_model = models.TextField(help_text="base64 decoded keras model for gap detection", null=True)

    class Meta:
        db_table = 'ml_solution'


class MLTrainingInformation(models.Model):
    id = models.AutoField(primary_key=True)
    ml_solution = models.ForeignKey(MLSolution, on_delete=models.CASCADE, help_text='model used')
    added_to = models.DateTimeField(auto_now_add=True, help_text='time it was added')
    training_time = models.IntegerField(help_text='training time of the model', null=True)
    iterations = models.IntegerField(help_text='iterations of the model has taken', null=True)
    target_iterations = models.IntegerField(help_text='max iteration set before end', null=True)
    target_accuracy = models.IntegerField(help_text='target accuracy of model', null=True)
    accuracy = models.FloatField(help_text='actual accuracy of the model', default=0.0)
    max_length = models.IntegerField(help_text="max size of elements this model can produce", null=True)
    image = models.TextField(help_text="base64 version of the image", null=True)
    prediction_length = models.IntegerField(help_text="prediction length used in forcasting", null=True)

    class Meta:
        db_table = 'ml_training_information'
