from django.urls import path  # new
from rest_framework.routers import DefaultRouter

from tsaAPI.views import tsd_configuration_graph_view as graph_view
from tsaAPI.views import tsd_configuration_view
from tsaAPI.views import tsd_model_view
from tsaAPI.views.tsd_training_information_view import TSDTrainingInformationViewSet

router = DefaultRouter()
router.register('tsd_model/<int:tsd_id>/tsd_training-information', TSDTrainingInformationViewSet)

urlpatterns = [
    path('tsd_model/', tsd_model_view.tsd_models_list, name='get a list of all tsa models'),
    path('tsd_model/<int:tsd_id>', tsd_model_view.tsd_models_by_id, name='get a list of all tsa models'),
    path('tsd_model/<int:tsd_id>/tsd_configuration/', tsd_configuration_view.config,
         name='GET, DELETE or PATCH model for id'),
    path('tsd_model/<int:tsd_id>/tsd_configuration/<int:pk>', tsd_configuration_view.get_config_object,
         name='GET, DELETE or PATCH model for id'),
    path('tsd_model/<int:tsd_id>/tsd_configuration/<int:pk>/copy', tsd_configuration_view.copy_config,
         name='POST copy of config'),

    path('tsd_model/<int:tsd_id>/tsd_configuration/<int:pk>/configure', graph_view.get_configuration_graph,
         name='GET configuration options for data'),
    path('tsd_model/<int:tsd_id>/tsd_configuration/<int:pk>/configure/<int:td>',
         graph_view.get_configuration_graph_for_train_data,
         name='GET configuration options for data'),
    path('tsd_model/<int:tsd_id>/tsd_configuration/<int:pk>/load_data',
         tsd_configuration_view.post_specific_level_for_config,
         name='GET configuration options for data'),
    path('tsd_model/<int:tsd_id>/tsd_configuration/<int:pk>/reduced_data/',
         tsd_configuration_view.get_data_reduced_values,
         name='get reduced information'),
    path('tsd_model/<int:tsd_id>/tsd_configuration/<int:pk>/preprocessor', tsd_configuration_view.handle_preprocessor,
         name='POST new preprocessor'),
    path('tsd_model/<int:tsd_id>/tsd_configuration/<int:pk>/add_levels/<int:td>',
         tsd_configuration_view.post_config_levels,
         name='POST level configuration to train data'),
]
