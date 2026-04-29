import unittest
from unittest.mock import patch, MagicMock
import subprocess
import sys
import os

# Mock colorama before importing utils
sys.modules['colorama'] = MagicMock()

# Add parent directory to path to allow importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.utils import check_tool

class TestUtils(unittest.TestCase):
    @patch('subprocess.run')
    def test_check_tool_installed(self, mock_run):
        # Setup mock to not raise an exception (success case)
        mock_run.return_value = subprocess.CompletedProcess(
            args=['which', 'ls'], returncode=0, stdout=b'/bin/ls\n', stderr=b''
        )

        result = check_tool('ls')

        self.assertTrue(result)
        mock_run.assert_called_once_with(["which", "ls"], capture_output=True, check=True)

    @patch('subprocess.run')
    def test_check_tool_not_installed(self, mock_run):
        # Setup mock to raise CalledProcessError
        mock_run.side_effect = subprocess.CalledProcessError(1, ['which', 'fake_tool'])

        result = check_tool('fake_tool')

        self.assertFalse(result)
        mock_run.assert_called_once_with(["which", "fake_tool"], capture_output=True, check=True)

    @patch('subprocess.run')
    def test_check_tool_exception(self, mock_run):
        # Setup mock to raise FileNotFoundError (e.g., if 'which' itself is not found)
        mock_run.side_effect = FileNotFoundError("No such file or directory: 'which'")

        result = check_tool('error_tool')

        self.assertFalse(result)
        mock_run.assert_called_once_with(["which", "error_tool"], capture_output=True, check=True)

if __name__ == '__main__':
    unittest.main()
