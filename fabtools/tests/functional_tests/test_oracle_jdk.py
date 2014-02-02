from fabtools.files import is_file
from fabtools.tests.vagrant_test_case import VagrantTestCase


class TestOracleJDK(VagrantTestCase):

    def test_require_default_jdk_version(self):

        from fabtools.oracle_jdk import version, DEFAULT_VERSION
        from fabtools.require.oracle_jdk import installed

        installed()

        self.assertTrue(is_file('/opt/jdk/bin/java'))
        self.assertEqual(version(), DEFAULT_VERSION)

    def test_require_jdk_version_6(self):

        from fabtools.oracle_jdk import version
        from fabtools.require.oracle_jdk import installed

        installed('6u45-b06')

        self.assertTrue(is_file('/opt/jdk/bin/java'))
        self.assertEqual(version(), '6u45-b06')
