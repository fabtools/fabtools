import os

from fabtools.files import is_file
from fabtools.tests.vagrant_test_case import VagrantTestCase


PATH = "/usr/share/tomcat"


class TestTomcat(VagrantTestCase):

    @classmethod
    def setUpClass(cls):
        from fabtools.require.oracle_jdk import installed
        installed()

    def test_tomcat_7_version(self):

        from fabtools.require.tomcat import installed
        from fabtools.tomcat import version, DEFAULT_VERSION

        installed()

        self.assertTrue(is_file(os.path.join(PATH, 'bin/catalina.sh')))
        self.assertEqual(version(PATH), DEFAULT_VERSION)

    def test_tomcat_6_version(self):

        TOMCAT6_VERSION = '6.0.36'

        from fabtools.require.tomcat import installed
        from fabtools.tomcat import version

        installed(version=TOMCAT6_VERSION)

        self.assertTrue(is_file(os.path.join(PATH, 'bin/catalina.sh')))
        self.assertEqual(version(PATH), TOMCAT6_VERSION)
