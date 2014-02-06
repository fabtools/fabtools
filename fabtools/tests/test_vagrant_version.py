import unittest

from mock import patch


class TestVagrantVersion(unittest.TestCase):

    def test_vagrant_version_1_3_0(self):
        with patch('fabtools.vagrant.local') as mock_local:
            mock_local.return_value = "Vagrant version 1.3.0\n"
            from fabtools.vagrant import version
            self.assertEqual(version(), (1, 3, 0))

    def test_vagrant_version_1_3_1(self):
        with patch('fabtools.vagrant.local') as mock_local:
            mock_local.return_value = "Vagrant v1.3.1\n"
            from fabtools.vagrant import version
            self.assertEqual(version(), (1, 3, 1))

    def test_vagrant_version_1_4_3(self):
        with patch('fabtools.vagrant.local') as mock_local:
            mock_local.return_value = "Vagrant 1.4.3\n"
            from fabtools.vagrant import version
            self.assertEqual(version(), (1, 4, 3))

    def test_vagrant_version_1_5_0_dev(self):
        with patch('fabtools.vagrant.local') as mock_local:
            mock_local.return_value = "Vagrant 1.5.0.dev\n"
            from fabtools.vagrant import version
            self.assertEqual(version(), (1, 5, 0, 'dev'))
