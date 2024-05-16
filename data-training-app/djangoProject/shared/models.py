from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)


class JwtUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    ROLE_CHOICES = [
        ('USER', 'User'),
        ('ADMIN', 'Admin')
    ]
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default="USER")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = '_user'


class TrainDataFile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, help_text='name representation for the frontend')
    user = models.ForeignKey(JwtUser, on_delete=models.CASCADE, help_text='User who owns this solution builder')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'train_data_file'
        unique_together = [['name', 'user']]


class TrainData(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(JwtUser, on_delete=models.CASCADE, help_text='User who owns this solution builder')
    name = models.CharField(max_length=50, help_text='name representation for the frontend')
    time_series_value = models.JSONField(help_text='value of dataset')
    time_stamp_value = models.JSONField(help_text='time stamps of dataset')
    file = models.ForeignKey(TrainDataFile, on_delete=models.CASCADE, help_text='file the current value belongs to')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'train_data'


class SchemaValidationForms(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, help_text="base schema name for usage")
    schema = models.JSONField(help_text="base json_schema, open to configuration")
    ui_schema = models.JSONField(help_text="ui option of the json schema")

    class Meta:
        db_table = "schema_validation_forms"


class PreprocessorType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, help_text="name of the preprocessor", unique=True)
    description = models.CharField(max_length=255, help_text="description of the preprocessor")
    schema_enum_value = models.CharField(max_length=50,
                                         help_text="string name of the value that is presented in the frontend")
    schema = models.JSONField(help_text="JSON_Schema of the object")

    class Meta:
        db_table = "preprocessor_type"


class ImputationAlgorithm(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, help_text="description of the imputation algorithm")

    class Meta:
        db_table = "imputation_algorithm"


class Preprocessor(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(PreprocessorType, on_delete=models.CASCADE, help_text="type")
    specific_config = models.JSONField(help_text="contains the specific configuration of the given preprocessor")

    class Meta:
        db_table = "preprocessor"


class Survey(models.Model):
    id: models.AutoField(primary_key=True)
    result = models.JSONField(help_text="survey results of the user")
    user = models.OneToOneField(JwtUser, on_delete=models.CASCADE, help_text='User who created the survey')

    class Meta:
        db_table = "survey"
