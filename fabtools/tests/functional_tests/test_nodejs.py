try:
    import json
except ImportError:
    import simplejson as json

import pytest

from fabric.api import cd, path, run

from fabtools.files import is_file

from fabtools.require import directory as require_directory
from fabtools.require import file as require_file


pytestmark = pytest.mark.network


@pytest.fixture
def nodejs(scope='module'):
    from fabtools.nodejs import install_from_source, version, DEFAULT_VERSION
    if version() != DEFAULT_VERSION:
        install_from_source()


def test_nodejs_is_installed(nodejs):

    from fabtools.nodejs import version, DEFAULT_VERSION

    assert is_file('/usr/local/bin/node')
    assert version() == DEFAULT_VERSION


def test_install_and_uninstall_global_package(nodejs):

    from fabtools.nodejs import install_package, package_version, uninstall_package

    # This is not in root's PATH on RedHat systems
    with path('/usr/local/bin'):

        if not package_version('underscore'):
            install_package('underscore', version='1.4.2')

        assert package_version('underscore') == '1.4.2'
        assert is_file('/usr/local/lib/node_modules/underscore/underscore.js')

        uninstall_package('underscore')

        assert package_version('underscore') is None
        assert not is_file('/usr/local/lib/node_modules/underscore/underscore.js')


def test_install_and_uninstall_local_package(nodejs):

    from fabtools.nodejs import install_package, package_version, uninstall_package

    if not package_version('underscore', local=True):
        install_package('underscore', version='1.4.2', local=True)

    assert is_file('node_modules/underscore/underscore.js')
    assert package_version('underscore', local=True) == '1.4.2'

    uninstall_package('underscore', local=True)

    assert package_version('underscore', local=True) is None
    assert not is_file('node_modules/underscore/underscore.js')


@pytest.yield_fixture
def testdir():
    require_directory('nodetest')
    yield 'nodetest'
    run('rm -rf nodetest')


def test_install_dependencies_from_package_json_file(nodejs, testdir):

    from fabtools.nodejs import install_dependencies, package_version, uninstall_package

    with cd(testdir):
        require_file('package.json', contents=json.dumps({
            'name': 'nodetest',
            'version': '1.0.0',
            'dependencies': {
                'underscore': '1.4.2'
            }
        }))

        install_dependencies()

        assert is_file('node_modules/underscore/underscore.js')
        assert package_version('underscore', local=True) == '1.4.2'

        uninstall_package('underscore', local=True)


def test_require_global_package(nodejs):

    from fabtools.require.nodejs import package as require_package
    from fabtools.nodejs import package_version, uninstall_package

    # This is not in root's PATH on RedHat systems
    with path('/usr/local/bin'):

        try:
            # Require specific version
            require_package('underscore', version='1.4.1')
            assert package_version('underscore') == '1.4.1'

            # Downgrade
            require_package('underscore', version='1.4.0')
            assert package_version('underscore') == '1.4.0'

            # Upgrade
            require_package('underscore', version='1.4.2')
            assert package_version('underscore') == '1.4.2'

        finally:
            uninstall_package('underscore')


def test_require_local_package(nodejs):

    from fabtools.require.nodejs import package as require_package
    from fabtools.nodejs import package_version, uninstall_package

    require_package('underscore', version='1.4.2', local=True)

    assert package_version('underscore', local=True) == '1.4.2'

    uninstall_package('underscore', local=True)
