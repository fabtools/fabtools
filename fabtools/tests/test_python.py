import mock
import unittest


class PythonTestCase(unittest.TestCase):

    @mock.patch('fabtools.python.run')
    def test_is_pip_installed_pythonbrew(self, mock_run):

        from fabric.operations import _AttributeString
        from fabtools.python import is_pip_installed

        fake_result = _AttributeString(
            '\x1b[32mSwitched to Python-2.7.5'
            '\x1b[0mpip 1.4.1 from /home/vagrant/.pythonbrew/pythons/Python-2.7.5/lib/python2.7/site-packages/pip-1.4.1-py2.7.egg (python 2.7)'
        )
        fake_result.failed = False
        fake_result.succeeded = True
        mock_run.return_value = fake_result

        res = is_pip_installed(version='1.3.1')

        self.assertTrue(res)
