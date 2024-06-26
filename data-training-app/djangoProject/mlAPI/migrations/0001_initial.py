# Generated by Django 4.2.4 on 2024-02-04 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MLConfiguration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='name representation for the frontend', max_length=50)),
                ('description', models.CharField(help_text='description of the model for the frontend', max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_running', models.CharField(help_text='if uuid = null, not running', max_length=50, null=True)),
                ('min_length', models.IntegerField(help_text='reduction value to which every dataset is trimmed before training', null=True)),
            ],
            options={
                'db_table': 'ml_configuration',
            },
        ),
        migrations.CreateModel(
            name='MLModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='name representation for the frontend', max_length=50)),
                ('description', models.CharField(help_text='description of the model for the frontend', max_length=255)),
                ('i18n_key', models.CharField(help_text='translation key for the description', max_length=50)),
                ('pyName', models.CharField(help_text='name of the python file that represents the model', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='created at')),
                ('forcasting', models.BooleanField(default=False, help_text='Not every model has forcast capabilities')),
            ],
            options={
                'db_table': 'ml_model',
            },
        ),
        migrations.CreateModel(
            name='MLSolution',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('generator_model', models.TextField(help_text='base64 decoded keras model')),
                ('gap_detector_model', models.TextField(help_text='base64 decoded keras model for gap detection', null=True)),
                ('ml_configuration', models.OneToOneField(help_text='id of the solution-builder', on_delete=django.db.models.deletion.CASCADE, to='mlAPI.mlconfiguration')),
            ],
            options={
                'db_table': 'ml_solution',
            },
        ),
        migrations.CreateModel(
            name='MLTrainingInformation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('added_to', models.DateTimeField(auto_now_add=True, help_text='time it was added')),
                ('training_time', models.IntegerField(help_text='training time of the model', null=True)),
                ('iterations', models.IntegerField(help_text='iterations of the model has taken', null=True)),
                ('target_iterations', models.IntegerField(help_text='max iteration set before end', null=True)),
                ('target_accuracy', models.IntegerField(help_text='target accuracy of model', null=True)),
                ('accuracy', models.FloatField(default=0.0, help_text='actual accuracy of the model')),
                ('max_length', models.IntegerField(help_text='max size of elements this model can produce', null=True)),
                ('image', models.TextField(help_text='base64 version of the image', null=True)),
                ('prediction_length', models.IntegerField(help_text='prediction length used in forcasting', null=True)),
                ('ml_solution', models.ForeignKey(help_text='model used', on_delete=django.db.models.deletion.CASCADE, to='mlAPI.mlsolution')),
            ],
            options={
                'db_table': 'ml_training_information',
            },
        ),
    ]
