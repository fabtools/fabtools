from __future__ import with_statement

try:
    import json
except ImportError:
    import simplejson as json

from fabric.api import *


@task
def install_nodejs():
    """
    Test low level API
    """

    from fabtools import nodejs
    from fabtools import require
    from fabtools.files import is_file

    # Install Node.js from source
    if nodejs.version() != nodejs.DEFAULT_VERSION:
        nodejs.install_from_source()

    assert is_file('/usr/local/bin/node')
    assert nodejs.version() == nodejs.DEFAULT_VERSION

    # Install / uninstall global package
    if not nodejs.package_version('underscore'):
        nodejs.install_package('underscore', version='1.4.2')

    assert nodejs.package_version('underscore') == '1.4.2'
    assert is_file('/usr/local/lib/node_modules/underscore/underscore.js')

    nodejs.uninstall_package('underscore')

    assert nodejs.package_version('underscore') is None
    assert not is_file('/usr/local/lib/node_modules/underscore/underscore.js')

    # Install / uninstall local package
    if not nodejs.package_version('underscore', local=True):
        nodejs.install_package('underscore', version='1.4.2', local=True)

    assert is_file('node_modules/underscore/underscore.js')
    assert nodejs.package_version('underscore', local=True) == '1.4.2'

    nodejs.uninstall_package('underscore', local=True)

    assert nodejs.package_version('underscore', local=True) is None
    assert not is_file('node_modules/underscore/underscore.js')

    # Install dependencies from package.json file
    require.directory('nodetest')
    with cd('nodetest'):
        require.file('package.json', contents=json.dumps({
            'name': 'nodetest',
            'version': '1.0.0',
            'dependencies': {
                'underscore': '1.4.2'
            }
        }))

        nodejs.install_dependencies()

        assert is_file('node_modules/underscore/underscore.js')
        assert nodejs.package_version('underscore', local=True) == '1.4.2'


@task
def require_nodejs():
    """
    Test high level API
    """

    from fabtools import nodejs
    from fabtools import require
    from fabtools.files import is_file

    # Require Node.js

    require.nodejs.installed_from_source()

    assert is_file('/usr/local/bin/node')
    assert nodejs.version() == nodejs.DEFAULT_VERSION

    # Require a global package

    nodejs.uninstall_package('underscore')

    require.nodejs.package('underscore', version='1.4.1')
    assert nodejs.package_version('underscore') == '1.4.1'

    require.nodejs.package('underscore', version='1.4.0')
    assert nodejs.package_version('underscore') == '1.4.0'

    require.nodejs.package('underscore', version='1.4.2')
    assert nodejs.package_version('underscore') == '1.4.2'

    # Require a local package

    nodejs.uninstall_package('underscore', local=True)

    require.nodejs.package('underscore', version='1.4.2', local=True)

    assert nodejs.package_version('underscore', local=True) == '1.4.2'
