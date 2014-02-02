from __future__ import with_statement

from fabtools.tests.vagrant_test_case import VagrantTestCase


class TestPython(VagrantTestCase):

    def test_require_setuptools(self):
        """
        Test Python setuptools installation
        """

        from fabtools import require

        require.python.setuptools()

    def test_require_virtualenv(self):
        """
        Test Python virtualenv creation
        """

        from fabtools import require
        import fabtools

        require.python.virtualenv('/tmp/venv')

        self.assertTrue(fabtools.files.is_dir('/tmp/venv'))
        self.assertTrue(fabtools.files.is_file('/tmp/venv/bin/python'))

    def test_require_python_package(self):
        """
        Test Python package installation
        """

        from fabtools import require
        import fabtools

        require.python.virtualenv('/tmp/venv')
        with fabtools.python.virtualenv('/tmp/venv'):
            require.python.package('fabric')

        self.assertTrue(fabtools.files.is_file('/tmp/venv/bin/fab'))
