from __future__ import with_statement

try:
    import json
except ImportError:
    import simplejson as json

from fabric.api import cd, run

from fabtools.files import is_file
from fabtools.require import directory as require_directory
from fabtools.require import file as require_file
from fabtools.tests.vagrant_test_case import VagrantTestCase


class NodeTestCase(VagrantTestCase):

    @classmethod
    def setUpClass(cls):
        from fabtools.nodejs import install_from_source, version, DEFAULT_VERSION
        if version() != DEFAULT_VERSION:
            install_from_source()

    @classmethod
    def tearDownClass(cls):
        from fabtools.nodejs import uninstall_package
        uninstall_package('underscore')
        uninstall_package('underscore', local=True)


class TestNodeJS(NodeTestCase):
    """
    Test low level API
    """

    def test_nodejs_is_installed(self):
        from fabtools.nodejs import version, DEFAULT_VERSION

        self.assertTrue(is_file('/usr/local/bin/node'))
        self.assertEqual(version(), DEFAULT_VERSION)

    def test_install_and_uninstall_global_package(self):
        from fabtools.nodejs import install_package, package_version, uninstall_package

        if not package_version('underscore'):
            install_package('underscore', version='1.4.2')

        self.assertEqual(package_version('underscore'), '1.4.2')
        self.assertTrue(is_file('/usr/local/lib/node_modules/underscore/underscore.js'))

        uninstall_package('underscore')

        self.assertIsNone(package_version('underscore'))
        self.assertFalse(is_file('/usr/local/lib/node_modules/underscore/underscore.js'))

    def test_install_and_uninstall_local_package(self):
        from fabtools.nodejs import install_package, package_version, uninstall_package

        if not package_version('underscore', local=True):
            install_package('underscore', version='1.4.2', local=True)

        self.assertTrue(is_file('node_modules/underscore/underscore.js'))
        self.assertEqual(package_version('underscore', local=True), '1.4.2')

        uninstall_package('underscore', local=True)

        self.assertIsNone(package_version('underscore', local=True))
        self.assertFalse(is_file('node_modules/underscore/underscore.js'))


class TestInstallDependencies(NodeTestCase):

    def setUp(self):
        require_directory('nodetest')

    def tearDown(self):
        run('rm -rf nodetest')

    def test_install_dependencies_from_package_json_file(self):
        from fabtools.nodejs import install_dependencies, package_version

        with cd('nodetest'):
            require_file('package.json', contents=json.dumps({
                'name': 'nodetest',
                'version': '1.0.0',
                'dependencies': {
                    'underscore': '1.4.2'
                }
            }))

            install_dependencies()

            self.assertTrue(is_file('node_modules/underscore/underscore.js'))
            self.assertEqual(package_version('underscore', local=True), '1.4.2')


class TestRequireNodeJS(NodeTestCase):
    """
    Test high level API
    """

    def test_nodejs_is_installed(self):
        from fabtools.nodejs import version, DEFAULT_VERSION

        self.assertTrue(is_file('/usr/local/bin/node'))
        self.assertEqual(version(), DEFAULT_VERSION)

    def test_require_global_package(self):
        from fabtools.require.nodejs import package as require_package
        from fabtools.nodejs import package_version

        # Require specific version
        require_package('underscore', version='1.4.1')
        self.assertEqual(package_version('underscore'), '1.4.1')

        # Downgrade
        require_package('underscore', version='1.4.0')
        self.assertEqual(package_version('underscore'), '1.4.0')

        # Upgrade
        require_package('underscore', version='1.4.2')
        self.assertEqual(package_version('underscore'), '1.4.2')

    def test_require_local_package(self):
        from fabtools.require.nodejs import package as require_package
        from fabtools.nodejs import package_version

        require_package('underscore', version='1.4.2', local=True)

        self.assertEqual(package_version('underscore', local=True), '1.4.2')
