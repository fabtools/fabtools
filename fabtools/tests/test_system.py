from __future__ import with_statement

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from mock import patch


class TestUnsupportedFamily(unittest.TestCase):

    def test_unsupported_system(self):

        from fabtools.system import UnsupportedFamily

        with self.assertRaises(UnsupportedFamily) as cm:

            with patch('fabtools.system.distrib_id') as mock_distrib_id:
                mock_distrib_id.return_value = 'foo'

                raise UnsupportedFamily(supported=['debian', 'redhat'])


        exception_msg = str(cm.exception)
        self.assertEquals(exception_msg, "Unsupported system foo (supported families: debian, redhat)")
