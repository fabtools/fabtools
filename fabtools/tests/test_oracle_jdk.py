
import mock
import unittest

from fabtools.oracle_jdk import _required_jdk_arch, _extract_jdk_version


class OracleJdkTestCase(unittest.TestCase):

    @mock.patch('fabtools.system.get_arch')
    def test_jdk_arch_for_x64_system(self, get_arch):
        get_arch.return_value = 'x86_64'

        self.assertEqual('x64', _required_jdk_arch())

    @mock.patch('fabtools.system.get_arch')
    def test_jdk_arch_for_32bit_system(self, get_arch):
        for system_arch in ['i386', 'i486', 'i586', 'i686']:
            get_arch.return_value = system_arch

            self.assertEqual('i586', _required_jdk_arch())

    @mock.patch('fabtools.system.get_arch')
    def test_jdk_arch_for_unknown_system(self, get_arch):
        get_arch.return_value = 'unknown'

        try:
            _required_jdk_arch()
            self.fail('Expected Exception was not raised')
        except Exception:
            pass

    def test_jdk_version_with_update_over_ten(self):
        java_version_out = '''java version "1.7.0_13"
Java(TM) SE Runtime Environment (build 1.7.0_13-b20)
Java HotSpot(TM) Client VM (build 23.7-b01, mixed mode)

'''

        self.assertEqual('7u13-b20', _extract_jdk_version(java_version_out))

    def test_jdk_version_with_update_under_ten(self):
        java_version_out = '''java version "1.7.0_09"
Java(TM) SE Runtime Environment (build 1.7.0_09-b05)
Java HotSpot(TM) 64-Bit Server VM (build 23.5-b02, mixed mode)
'''

        self.assertEqual('7u9-b05', _extract_jdk_version(java_version_out))
