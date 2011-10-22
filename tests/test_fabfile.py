try:
    import unittest2 as unittest
except ImportError:
    import unittest

from fabric.api import *

from vagrant import VagrantTestCase, VagrantTestSuite
import fabfile


class TestMySQL(VagrantTestCase):

    def setUp(self):
        """
        Clean up MySQL install before tests
        """
        with self._suite.settings(hide('running', 'stdout')):
            sudo("aptitude remove --assume-yes --purge mysql-server-5.1")

    def runTest(self):
        """
        Run the 'mysql' task from the fabfile
        """
        fabfile.mysql()


class TestPostgreSQL(VagrantTestCase):

    def setUp(self):
        """
        Clean up PostgreSQL install before tests
        """
        with self._suite.settings(hide('running', 'stdout')):
            sudo("aptitude remove --assume-yes --purge postgresql")

    def runTest(self):
        """
        Run the 'postgresql' task from the fabfile
        """
        fabfile.postgresql()


def load_tests(loader, tests, patterns):
    suite = VagrantTestSuite(['ubuntu_10_04', 'ubuntu_10_10'])
    suite.addTest(TestMySQL(suite))
    suite.addTest(TestPostgreSQL(suite))
    return suite


if __name__ == '__main__':
    unittest.main()
