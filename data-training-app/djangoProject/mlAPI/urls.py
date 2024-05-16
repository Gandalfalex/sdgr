from django.contrib import admin
from django.urls import path, include  # new
from .views import ml_model_view, ml_solution_builder_view, ml_configuration_view, \
    training_information_view

urlpatterns = [
    path('ml_model', ml_model_view.mlmodels_list, name='get a list of all ml models'),
    path('ml_model/', ml_model_view.post_new_model, name='post new model'),
    path('ml_model/<int:pk>', ml_model_view.mlmodels_detail, name='get specific model'),

    path('ml_model/<int:m_id>/ml_solution/', ml_solution_builder_view.configuration_view, name='POST = new builder'),
    path('ml_model/<int:m_id>/ml_solution/<int:pk>', ml_solution_builder_view.get_solution_object, name='GET, DELETE or PATCH model for id'),
    path('ml_model/<int:m_id>/ml_solution/<int:pk>/copy', ml_solution_builder_view.copy_solution, name='Copy model by id'),
    path('ml_model/<int:m_id>/ml_solution/<int:pk>/preprocessor', ml_solution_builder_view.handle_preprocessor, name='POST, GET, DELETE or PATCH new preprocessor'),

    path('ml_model/<int:m_id>/ml_solution/<int:pk>/reduced_data', ml_solution_builder_view.get_data_reduced_values, name='GET a list of trainings data in a reduced form'),
    path('ml_model/<int:m_id>/config/<int:c_id>', training_information_view.get_information_by_config_id, name='GET trainings information'),
    path('ml_model/<int:m_id>/ml_solution/<int:pk>/ml_configuration/load_data', ml_configuration_view.load_config, name='load config and generate data')
]
