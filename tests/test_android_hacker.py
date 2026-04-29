import sys
import unittest
from unittest.mock import patch, MagicMock

# Mock colorama since it's not available in the test environment
mock_colorama = MagicMock()
sys.modules['colorama'] = mock_colorama

import android_hacker

class TestAndroidHackerFramework(unittest.TestCase):
    @patch('android_hacker.AndroidHackerFramework.clear_screen')
    def setUp(self, mock_clear_screen):
        self.framework = android_hacker.AndroidHackerFramework()

    @patch('subprocess.run')
    def test_get_local_ip_192_168_prefix(self, mock_subprocess_run):
        mock_result = MagicMock()
        mock_result.stdout = "192.168.1.50"
        mock_subprocess_run.return_value = mock_result

        ip = self.framework.get_local_ip()
        self.assertEqual(ip, "192.168.1.50")

    @patch('subprocess.run')
    def test_get_local_ip_10_prefix(self, mock_subprocess_run):
        mock_result = MagicMock()
        mock_result.stdout = "10.0.0.5"
        mock_subprocess_run.return_value = mock_result

        ip = self.framework.get_local_ip()
        self.assertEqual(ip, "10.0.0.5")

    @patch('subprocess.run')
    def test_get_local_ip_multiple_ips(self, mock_subprocess_run):
        mock_result = MagicMock()
        # Should pick the first valid one
        mock_result.stdout = "172.17.0.1 192.168.2.100 10.0.0.1"
        mock_subprocess_run.return_value = mock_result

        ip = self.framework.get_local_ip()
        self.assertEqual(ip, "192.168.2.100")

    @patch('subprocess.run')
    def test_get_local_ip_no_matching_prefix(self, mock_subprocess_run):
        mock_result = MagicMock()
        mock_result.stdout = "172.17.0.1 127.0.0.1"
        mock_subprocess_run.return_value = mock_result

        ip = self.framework.get_local_ip()
        self.assertEqual(ip, "192.168.1.108")

    @patch('subprocess.run')
    def test_get_local_ip_empty_stdout(self, mock_subprocess_run):
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_subprocess_run.return_value = mock_result

        ip = self.framework.get_local_ip()
        self.assertEqual(ip, "192.168.1.108")

    @patch('subprocess.run')
    def test_get_local_ip_exception(self, mock_subprocess_run):
        mock_subprocess_run.side_effect = Exception("Command failed")

        ip = self.framework.get_local_ip()
        self.assertEqual(ip, "192.168.1.108")

if __name__ == '__main__':
    unittest.main()
