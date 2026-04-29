import unittest
from unittest.mock import patch
import os
from modules.utils import check_root

class TestUtils(unittest.TestCase):

    @patch('os.geteuid')
    def test_check_root_is_root(self, mock_geteuid):
        mock_geteuid.return_value = 0
        self.assertTrue(check_root())

    @patch('os.geteuid')
    @patch('builtins.print')
    def test_check_root_not_root(self, mock_print, mock_geteuid):
        mock_geteuid.return_value = 1000
        self.assertFalse(check_root())
        mock_print.assert_called_once()

if __name__ == '__main__':
    unittest.main()
