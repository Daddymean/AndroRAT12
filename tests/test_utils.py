import unittest
import os
import sys
import subprocess
from unittest.mock import patch, MagicMock

# Mock colorama before importing modules.utils
with patch.dict('sys.modules', {'colorama': MagicMock()}):
    from modules.utils import check_root, get_local_ip, check_tool, install_tool, create_directory

class TestUtils(unittest.TestCase):
    @patch('os.geteuid')
    @patch('builtins.print')
    def test_check_root_as_root(self, mock_print, mock_geteuid):
        mock_geteuid.return_value = 0
        self.assertTrue(check_root())
        mock_print.assert_not_called()

    @patch('os.geteuid')
    @patch('builtins.print')
    def test_check_root_as_non_root(self, mock_print, mock_geteuid):
        mock_geteuid.return_value = 1000
        self.assertFalse(check_root())
        mock_print.assert_called()

    @patch('socket.socket')
    def test_get_local_ip_success(self, mock_socket):
        mock_s = MagicMock()
        mock_socket.return_value = mock_s
        mock_s.getsockname.return_value = ("192.168.1.100", 12345)

        ip = get_local_ip()
        self.assertEqual(ip, "192.168.1.100")

    @patch('socket.socket')
    def test_get_local_ip_failure(self, mock_socket):
        mock_socket.side_effect = Exception("Connection failed")

        ip = get_local_ip()
        self.assertEqual(ip, "127.0.0.1")

    @patch('subprocess.run')
    def test_check_tool_installed(self, mock_run):
        mock_run.return_value = MagicMock()

        self.assertTrue(check_tool("ls"))

    @patch('subprocess.run')
    def test_check_tool_not_installed(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, "which")

        self.assertFalse(check_tool("nonexistent_tool"))

    @patch('subprocess.run')
    @patch('builtins.print')
    def test_install_tool(self, mock_print, mock_run):
        install_tool("git")
        mock_run.assert_called_with(["sudo", "apt", "install", "-y", "git"], capture_output=True)
        mock_print.assert_called()

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_create_directory_not_exists(self, mock_makedirs, mock_exists):
        mock_exists.return_value = False
        create_directory("test_dir")
        mock_makedirs.assert_called_with("test_dir")

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_create_directory_exists(self, mock_makedirs, mock_exists):
        mock_exists.return_value = True
        create_directory("test_dir")
        mock_makedirs.assert_not_called()

if __name__ == '__main__':
    unittest.main()
