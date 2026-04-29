import unittest
from unittest.mock import patch, MagicMock
import sys

# Mock colorama
sys.modules['colorama'] = MagicMock()

from android_hacker import AndroidHackerFramework

class TestIPDiscovery(unittest.TestCase):

    @patch('socket.socket')
    def test_get_local_ip_success(self, mock_socket):
        # Setup mock
        mock_s = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_s
        mock_s.getsockname.return_value = ['192.168.1.50']

        # Call method
        ip = AndroidHackerFramework.get_local_ip(None)

        # Verify
        self.assertEqual(ip, '192.168.1.50')
        mock_s.connect.assert_called_with(('8.8.8.8', 1))

    @patch('socket.socket')
    def test_get_local_ip_failure(self, mock_socket):
        # Setup mock to raise exception
        mock_socket.side_effect = Exception("Socket error")

        # Call method
        ip = AndroidHackerFramework.get_local_ip(None)

        # Verify fallback
        self.assertEqual(ip, "192.168.1.108")

if __name__ == '__main__':
    unittest.main()
