import sys
import unittest
from unittest.mock import patch, MagicMock

# Mock colorama module before importing utils
sys.modules['colorama'] = MagicMock()

from modules.utils import get_local_ip

class TestGetLocalIp(unittest.TestCase):
    @patch('socket.socket')
    def test_get_local_ip_success(self, mock_socket_class):
        # Create a mock socket instance
        mock_socket_instance = MagicMock()
        mock_socket_class.return_value = mock_socket_instance

        # Configure the mock instance to return a specific IP
        mock_socket_instance.getsockname.return_value = ('192.168.1.100', 12345)

        # Call the function
        ip = get_local_ip()

        # Assertions
        self.assertEqual(ip, '192.168.1.100')
        mock_socket_class.assert_called_once()
        mock_socket_instance.connect.assert_called_once_with(("8.8.8.8", 80))
        mock_socket_instance.getsockname.assert_called_once()
        mock_socket_instance.close.assert_called_once()

    @patch('socket.socket')
    def test_get_local_ip_failure(self, mock_socket_class):
        # Configure socket to raise an exception on connect
        mock_socket_instance = MagicMock()
        mock_socket_class.return_value = mock_socket_instance
        mock_socket_instance.connect.side_effect = Exception("Network error")

        # Call the function
        ip = get_local_ip()

        # Assertions
        self.assertEqual(ip, '127.0.0.1')
        mock_socket_class.assert_called_once()
        mock_socket_instance.connect.assert_called_once_with(("8.8.8.8", 80))

if __name__ == '__main__':
    unittest.main()
