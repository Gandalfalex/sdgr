import unittest
from unittest.mock import patch, Mock, MagicMock

from shared.models import TrainData
from shared.services.database_service import get_train_data, NotFoundException
from django.db.models import ObjectDoesNotExist


class GetTrainDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(GetTrainDataTest, cls).setUpClass()
        cls.global_user = MagicMock()
        cls.global_user.id = 1

    @patch('shared.models.TrainData.objects.get')
    def test_train_data_exists(self, mock_get):
        mock_get.return_value = "Data exists"

        result = get_train_data(123, self.global_user.id)
        mock_get.assert_called_with(pk=123, user=self.global_user.id)

        self.assertEqual("Data exists", result)

    @patch('shared.models.TrainData.objects.get')
    def test_train_data_does_not_exist(self, mock_get):
        mock_get.side_effect = TrainData.DoesNotExist()

        with self.assertRaises(NotFoundException):
            get_train_data(123, self.global_user.id)
