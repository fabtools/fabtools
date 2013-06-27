
import mock
import unittest


class OracleJdkTestCase(unittest.TestCase):

    @mock.patch('fabtools.oracle_jdk.get_arch')
    def test_jdk_arch_for_x64_system(self, get_arch):

        from fabtools.oracle_jdk import _required_jdk_arch

        get_arch.return_value = 'x86_64'

        self.assertEqual('x64', _required_jdk_arch())

    @mock.patch('fabtools.oracle_jdk.get_arch')
    def test_jdk_arch_for_32bit_system(self, get_arch):

        from fabtools.oracle_jdk import _required_jdk_arch

        for system_arch in ['i386', 'i486', 'i586', 'i686']:

            get_arch.return_value = system_arch

            self.assertEqual('i586', _required_jdk_arch())

    @mock.patch('fabtools.oracle_jdk.get_arch')
    def test_jdk_arch_for_unknown_system(self, get_arch):

        from fabtools.oracle_jdk import _required_jdk_arch

        get_arch.return_value = 'unknown'

        self.assertRaises(Exception, _required_jdk_arch)

    def test_jdk_version_with_update_over_ten(self):

        from fabtools.oracle_jdk import _extract_jdk_version

        java_version_out = '''java version "1.7.0_13"
Java(TM) SE Runtime Environment (build 1.7.0_13-b20)
Java HotSpot(TM) Client VM (build 23.7-b01, mixed mode)

'''

        self.assertEqual('7u13-b20', _extract_jdk_version(java_version_out))

    def test_jdk_version_with_update_under_ten(self):

        from fabtools.oracle_jdk import _extract_jdk_version

        java_version_out = '''java version "1.7.0_09"
Java(TM) SE Runtime Environment (build 1.7.0_09-b05)
Java HotSpot(TM) 64-Bit Server VM (build 23.5-b02, mixed mode)
'''

        self.assertEqual('7u9-b05', _extract_jdk_version(java_version_out))

    def test_jdk_version_with_openjdk(self):

        from fabtools.oracle_jdk import _extract_jdk_version

        java_version_out = '''java version "1.7.0_21"
OpenJDK Runtime Environment (IcedTea 2.3.9) (7u21-2.3.9-0ubuntu0.12.04.1)
OpenJDK 64-Bit Server VM (build 23.7-b01, mixed mode)
'''

        self.assertEqual(None, _extract_jdk_version(java_version_out))
