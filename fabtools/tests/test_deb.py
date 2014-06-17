import unittest

from mock import patch


class AptKeyTestCase(unittest.TestCase):

    def test_key_length(self):
        from fabtools.deb import _validate_apt_key

        self.assertRaises(ValueError, _validate_apt_key, "ABC123")
        self.assertRaises(ValueError, _validate_apt_key, "ABCDE12345")
        self.assertEqual(_validate_apt_key("ABCD1234"), None)
