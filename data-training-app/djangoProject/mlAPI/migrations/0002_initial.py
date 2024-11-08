# Generated by Django 4.2.4 on 2024-02-04 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shared', '0001_initial'),
        ('mlAPI', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlconfiguration',
            name='imputation_algorithm',
            field=models.ForeignKey(help_text='algorithm used to impute data', null=True, on_delete=django.db.models.deletion.SET_NULL, to='shared.imputationalgorithm'),
        ),
        migrations.AddField(
            model_name='mlconfiguration',
            name='ml_model',
            field=models.ForeignKey(help_text='model used for this configuration', on_delete=django.db.models.deletion.CASCADE, to='mlAPI.mlmodel'),
        ),
        migrations.AddField(
            model_name='mlconfiguration',
            name='processing',
            field=models.OneToOneField(help_text='preprocessing to speed up training', null=True, on_delete=django.db.models.deletion.CASCADE, to='shared.preprocessor'),
        ),
        migrations.AddField(
            model_name='mlconfiguration',
            name='train_data',
            field=models.ManyToManyField(help_text='n:m, training data for the model', to='shared.traindata'),
        ),
        migrations.AddField(
            model_name='mlconfiguration',
            name='user',
            field=models.ForeignKey(help_text='User who owns this solution builder', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
