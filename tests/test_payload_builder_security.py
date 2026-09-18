import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Mock colorama before importing PayloadBuilder
sys.modules['colorama'] = MagicMock()

from modules.payload_builder import PayloadBuilder

class TestPayloadBuilderSecurity(unittest.TestCase):
    def setUp(self):
        self.builder = PayloadBuilder("127.0.0.1", 4444, "test_payload")
        self.pass_file = ".keystore_pass"
        if os.path.exists(self.pass_file):
            os.remove(self.pass_file)
        if "ANDROID_KEYSTORE_PASS" in os.environ:
            del os.environ["ANDROID_KEYSTORE_PASS"]

    def tearDown(self):
        if os.path.exists(self.pass_file):
            os.remove(self.pass_file)
        if "ANDROID_KEYSTORE_PASS" in os.environ:
            del os.environ["ANDROID_KEYSTORE_PASS"]

    def test_get_keystore_password_generates_new_pass(self):
        password = self.builder._get_keystore_password()
        self.assertEqual(len(password), 16)
        self.assertTrue(os.path.exists(self.pass_file))

        # Check permissions
        mode = os.stat(self.pass_file).st_mode
        self.assertEqual(oct(mode & 0o777), '0o600')

        with open(self.pass_file, "r") as f:
            file_content = f.read()
        self.assertEqual(password, file_content)

    def test_get_keystore_password_uses_existing_file(self):
        preset_pass = "preset_password"
        with open(self.pass_file, "w") as f:
            f.write(preset_pass)

        password = self.builder._get_keystore_password()
        self.assertEqual(password, preset_pass)

    def test_get_keystore_password_uses_env_var(self):
        env_pass = "env_password"
        os.environ["ANDROID_KEYSTORE_PASS"] = env_pass

        password = self.builder._get_keystore_password()
        self.assertEqual(password, env_pass)

    @patch('subprocess.run')
    def test_create_keystore_uses_dynamic_password(self, mock_run):
        os.environ["ANDROID_KEYSTORE_PASS"] = "secret123"
        self.builder.create_keystore()

        # Check if subprocess.run was called with the correct password
        called_args = mock_run.call_args[0][0]
        self.assertIn("secret123", called_args)
        self.assertNotIn("android", called_args)

    @patch('subprocess.run')
    @patch('os.path.exists')
    @patch('os.remove')
    @patch('shutil.copy')
    def test_sign_apk_uses_dynamic_password(self, mock_copy, mock_remove, mock_exists, mock_run):
        os.environ["ANDROID_KEYSTORE_PASS"] = "secret456"
        # Mocking file existence to bypass checks
        # We want to trigger the fallback to jarsigner too
        mock_exists.side_effect = lambda x: True if "_final.apk" not in x else False

        self.builder.sign_apk("test")

        # Check apksigner call
        apksigner_call = None
        jarsigner_call = None
        for call in mock_run.call_args_list:
            args = call[0][0]
            if "apksigner" in args:
                apksigner_call = args
            if "jarsigner" in args:
                jarsigner_call = args

        if apksigner_call:
            self.assertIn("pass:secret456", apksigner_call)
            self.assertNotIn("pass:android", apksigner_call)

        if jarsigner_call:
            self.assertIn("secret456", jarsigner_call)
            self.assertNotIn("android", jarsigner_call)

if __name__ == "__main__":
    unittest.main()
