import unittest
from shared.services.training_data_service import get_training_data_by_ids
from unittest.mock import patch, Mock


class TestTrainingDataService(unittest.TestCase):

    @patch('shared.services.training_data_service.get_train_data')
    def test_get_training_data_by_ids_returns_valid_data(self, mock_get_train_data):
        # Assuming get_train_data returns a dictionary with id and user
        mock_get_train_data.return_value = {'id': 1, 'user': 'test_user'}

        ids = [1, 2, 3]
        user = 'test_user'

        result = get_training_data_by_ids(ids, user)
        expected_result = [{'id': 1, 'user': 'test_user'}, {'id': 1, 'user': 'test_user'},
                           {'id': 1, 'user': 'test_user'}]

        self.assertEqual(result, expected_result)

    @patch('shared.services.training_data_service.get_train_data')
    def test_get_training_data_by_ids_returns_none_on_invalid_id(self, mock_get_train_data):
        # get_train_data returns None for invalid id
        mock_get_train_data.return_value = None

        ids = [10, 20, 30]  # Assuming these are invalid ids
        user = 'test_user'

        result = get_training_data_by_ids(ids, user)

        self.assertEqual(result, [None, None, None])

    @patch('shared.services.training_data_service.get_train_data')
    def test_get_training_data_by_ids_raises_exception_on_invalid_id(self, mock_get_train_data):
        # get_train_data raises an Exception for invalid id
        mock_get_train_data.side_effect = Exception('Invalid Id provided')

        ids = [10, 20, 30]  # Assuming these are invalid ids
        user = 'test_user'

        with self.assertRaises(Exception) as context:
            get_training_data_by_ids(ids, user)

        self.assertTrue('Invalid Id provided' in str(context.exception))


if __name__ == '__main__':
    unittest.main()