from django.urls import path
from shared.views import train_data_view, preprocessor_view, config_preview_view, survey_view

urlpatterns = [
    path('preprocessor/upload', config_preview_view.create, name='upload your training data'),
    path('preprocessor/', preprocessor_view.get_all_preprocessor_types, name='get all preprocessor_types'),
    path('preprocessor/', preprocessor_view.save_all_preprocessor_types, name='save new preprocessor_type'),
    path('preprocessor/<int:type_id>', preprocessor_view.get_preprocessor_type, name='get a single preprocessor_types'),
    path('training_data/upload', train_data_view.upload_data, name='upload your training data'),
    path('training_data/', train_data_view.get_train_data_request, name='get a list of all your training data'),
    path('training_data/files', train_data_view.get_user_files, name='get a list of your training data files'),
    path('training_data/files/<int:pk>', train_data_view.get_elements_of_user_file, name='get a list of your training data files'),
    path('training_data/<int:pk>', train_data_view.get_specific_train_data, name='get a single training data object'),
    path('training_data/<int:pk>/information', train_data_view.get_train_data_information,
         name='receive information of the traindata'),
    path('survey', survey_view.post_survey, name='add survey')
]
