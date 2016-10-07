"""
Node.js
=======

This module provides tools for installing `Node.js`_ and managing
packages using `npm`_.

.. note: the ``simplejson`` module is required on Python 2.5

.. _Node.js: http://nodejs.org/
.. _npm: http://npmjs.org/

"""

try:
    import json
except ImportError:
    import simplejson as json

from fabric.api import cd, hide, run, settings

from fabtools.system import cpus, distrib_family
from fabtools.utils import run_as_root


DEFAULT_VERSION = '0.10.13'


def install_from_source(version=DEFAULT_VERSION, checkinstall=False):
    """
    Install Node JS from source.

    If *checkinstall* is ``True``, a distribution package will be built.

    ::

        import fabtools

        # Install Node.js
        fabtools.nodejs.install_nodejs()

    .. note:: This function may not work for old versions of Node.js.

    """

    from fabtools.require.deb import packages as require_deb_packages
    from fabtools.require.rpm import packages as require_rpm_packages
    from fabtools.require import file as require_file

    family = distrib_family()

    if family == 'debian':
        packages = [
            'build-essential',
            'libssl-dev',
            'python',
        ]
        if checkinstall:
            packages.append('checkinstall')
        require_deb_packages(packages)

    elif family == 'redhat':
        packages = [
            'gcc',
            'gcc-c++',
            'make',
            'openssl-devel',
            'python',
        ]
        if checkinstall:
            packages.append('checkinstall')
        require_rpm_packages(packages)

    filename = 'node-v%s.tar.gz' % version
    foldername = filename[0:-7]

    require_file(url='http://nodejs.org/dist/v%(version)s/%(filename)s' % {
        'version': version,
        'filename': filename,
    })
    run('tar -xzf %s' % filename)
    with cd(foldername):
        run('./configure')
        run('make -j%d' % (cpus() + 1))
        if checkinstall:
            run_as_root(
                'checkinstall -y --pkgname=nodejs --pkgversion=%(version) '
                '--showinstall=no make install' % locals())
        else:
            run_as_root('make install')
    run('rm -rf %(filename)s %(foldername)s' % locals())


def version(node='node'):
    """
    Get the version of Node.js currently installed.

    Returns ``None`` if it is not installed.
    """
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        res = run('%(node)s --version' % locals())
    if res.failed:
        return None
    else:
        return res[1:]


def install_package(package, version=None, local=False, npm='npm'):
    """
    Install a Node.js package.

    If *local* is ``True``, the package will be installed locally.

    ::

        import fabtools

        # Install package globally
        fabtools.nodejs.install_package('express')

        # Install package locally
        fabtools.nodejs.install_package('underscore', local=False)

    """
    if version:
        package += '@%s' % version

    if local:
        run('%(npm)s install -l %(package)s' % locals())
    else:
        run_as_root('HOME=/root %(npm)s install -g %(package)s' % locals())


def install_dependencies(npm='npm'):
    """
    Install Node.js package dependencies.

    This function calls ``npm install``, which will locally install all
    packages specified as dependencies in the ``package.json`` file
    found in the current directory.

    ::

        from fabric.api import cd
        from fabtools import nodejs

        with cd('/path/to/nodejsapp/'):
            nodejs.install_dependencies()

    """
    run('%(npm)s install' % locals())


def package_version(package, local=False, npm='npm'):
    """
    Get the installed version of a Node.js package.

    Returns ``None``is the package is not installed. If *local* is
    ``True``, returns the version of the locally installed package.
    """
    options = ['--json true', '--silent']
    if local:
        options.append('-l')
    else:
        options.append('-g')
    options = ' '.join(options)

    with hide('running', 'stdout'):
        res = run('%(npm)s list %(options)s' % locals(), pty=False)

    dependencies = json.loads(res).get('dependencies', {})
    pkg_data = dependencies.get(package)
    if pkg_data:
        return pkg_data['version']
    else:
        return None


def update_package(package, local=False, npm='npm'):
    """
    Update a Node.js package.

    If *local* is ``True``, the package will be updated locally.
    """
    if local:
        run('%(npm)s update -l %(package)s' % locals())
    else:
        run_as_root('HOME=/root %(npm)s update -g %(package)s' % locals())


def uninstall_package(package, version=None, local=False, npm='npm'):
    """
    Uninstall a Node.js package.

    If *local* is ``True``, the package will be uninstalled locally.

    ::

        import fabtools

        # Uninstall package globally
        fabtools.nodejs.uninstall_package('express')

        # Uninstall package locally
        fabtools.nodejs.uninstall_package('underscore', local=False)

    """
    if version:
        package += '@%s' % version

    if local:
        run('%(npm)s uninstall -l %(package)s' % locals())
    else:
        run_as_root('HOME=/root %(npm)s uninstall -g %(package)s' % locals())
