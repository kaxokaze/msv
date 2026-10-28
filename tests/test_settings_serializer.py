"""Local-only tests for XML settings conversion."""
import tempfile
import os
import unittest

from svLib.userData.svSettingsSerializer import convert_to_type


class SettingsSerializerTests(unittest.TestCase):
    def test_bool_conversion_is_case_sensitive_and_explicit(self):
        self.assertTrue(convert_to_type("True", "builtins.bool"))
        self.assertFalse(convert_to_type("False", "builtins.bool"))

    def test_numeric_conversion(self):
        self.assertEqual(convert_to_type("2.5", "builtins.float"), 2.5)
        self.assertEqual(convert_to_type("42", "builtins.int"), 42)


if __name__ == "__main__":
    unittest.main()
