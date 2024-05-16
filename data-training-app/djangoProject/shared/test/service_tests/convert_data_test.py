import unittest
import numpy as np
from unittest.mock import patch, mock_open, Mock, MagicMock

from shared.models import JwtUser
from shared.services.training_data_service import build_data_to_interest


class ConvertDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(ConvertDataTest, cls).setUpClass()
        cls.global_user = MagicMock()
        cls.global_user.id = 1
        cls.global_user.email = 'test@example.com'
        cls.global_user.password = 'password'
        cls.global_user.first_name = 'Test'
        cls.global_user.last_name = 'User'
        cls.global_user.role = 'USER'



    @patch('shared.services.database_service.get_train_data')
    @patch("shared.preprocessing.gap_processing.gap_processing.contains_gaps")
    @patch("shared.strategies.gap_detection_strategy.get_imputation_algorithm_strategy")
    @patch("shared.preprocessing.gap_processing.gap_processing.__find_differences_in_steps_and_fill_them_with_nan")
    @patch("shared.preprocessing.gap_processing.gap_processing.remove_gaps_if_existing")
    def test_build_data_to_interest(self, mock_remove_gaps_if_existing,
                                    mock_find_differences_in_steps_and_fill_them_with_nan,
                                    mock_get_imputation_algorithm_strategy, mock_contains_gaps, mock_get_train_data):
        # Set up mock objects
        mock_get_train_data.return_value.time_series_value = [1, 2, 3]
        mock_get_train_data.return_value.time_stamp_value = [10, 20, 30]
        mock_contains_gaps.return_value = True
        mock_get_imputation_algorithm_strategy.return_value = "MEDIAN"
        mock_find_differences_in_steps_and_fill_them_with_nan.return_value = (
            [np.array(["NaN", 2, 3])], [np.array([10, 20, 30])])
        mock_remove_gaps_if_existing.return_value = ([np.array([1.0, 2.0, 3.0])], [np.array([10.0, 20.0, 30.0])], 3)

        # Call the function
        result = build_data_to_interest(3, ConvertDataTest.global_user.id)

        # Assert the expected result
        expected_result = {
            "original": {"name": "original", "values": [1.0, 2.0, 3.0]},
            "flags": [True, False, False]
        }
        self.assertEqual(result, expected_result)

        # Assert the function calls
        mock_get_train_data.assert_called_once_with(123, "currentUser")
        mock_contains_gaps.assert_called_once_with([np.array([10, 20, 30])])
        mock_get_imputation_algorithm_strategy.assert_called_once_with("MEDIAN")
        mock_find_differences_in_steps_and_fill_them_with_nan.assert_called_once_with([np.array([1, 2, 3])],
                                                                                      [np.array([10, 20, 30])])
        mock_remove_gaps_if_existing.assert_called_once_with([np.array([1, 2, 3])], [np.array([10, 20, 30])], "MEDIAN")


# Runs the unit tests
if __name__ == '__main__':
    unittest.main()
