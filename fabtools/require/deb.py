"""
Debian packages
===============

This module provides high-level tools for managing Debian/Ubuntu packages
and repositories.

"""
from __future__ import with_statement

from fabric.utils import puts

from fabtools.deb import (
    add_apt_key,
    apt_key_exists,
    install,
    is_installed,
    uninstall,
    update_index,
)
from fabtools.files import is_file, watch
from fabtools.system import distrib_codename
from fabtools.utils import run_as_root


def key(keyid, filename=None, url=None, keyserver='subkeys.pgp.net', update=False):
    """
    Require a PGP key for APT.

    ::

        from fabtools import require

        # Varnish signing key from URL
        require.deb.key('C4DEFFEB', url='http://repo.varnish-cache.org/debian/GPG-key.txt')

        # Nginx signing key from default key server (subkeys.pgp.net)
        require.deb.key('7BD9BF62')

        # From custom key server
        require.deb.key('7BD9BF62', keyserver='keyserver.ubuntu.com')

        # From file
        require.deb.key('7BD9BF62', filename='nginx.asc')

    """

    if not apt_key_exists(keyid):
        add_apt_key(keyid=keyid, filename=filename, url=url, keyserver=keyserver, update=update)


def source(name, uri, distribution, *components):
    """
    Require a package source.

    ::

        from fabtools import require

        # Official MongoDB packages
        require.deb.source('mongodb', 'http://downloads-distro.mongodb.org/repo/ubuntu-upstart', 'dist', '10gen')

    """

    from fabtools.require import file as require_file

    path = '/etc/apt/sources.list.d/%(name)s.list' % locals()
    components = ' '.join(components)
    source_line = 'deb %(uri)s %(distribution)s %(components)s\n' % locals()
    with watch(path) as config:
        require_file(path=path, contents=source_line, use_sudo=True)
    if config.changed:
        puts('Added APT repository: %s' % source_line)
        update_index()


def ppa(name):
    """
    Require a `PPA`_ package source.

    Example::

        from fabtools import require

        # Node.js packages by Chris Lea
        require.deb.ppa('ppa:chris-lea/node.js')

    .. _PPA: https://help.launchpad.net/Packaging/PPA
    """
    assert name.startswith('ppa:')
    user, repo = name[4:].split('/', 2)
    distrib = distrib_codename()
    source = '%(user)s-%(repo)s-%(distrib)s.list' % locals()

    if not is_file(source):
        package('python-software-properties')
        run_as_root('add-apt-repository %s' % name, pty=False)
        update_index()


def package(pkg_name, update=False, version=None):
    """
    Require a deb package to be installed.

    Example::

        from fabtools import require

        # Require a package
        require.deb.package('foo')

        # Require a specific version
        require.deb.package('firefox', version='11.0+build1-0ubuntu4')

    """
    if not is_installed(pkg_name):
        install(pkg_name, update=update, version=version)


def packages(pkg_list, update=False):
    """
    Require several deb packages to be installed.

    Example::

        from fabtools import require

        require.deb.packages([
            'foo',
            'bar',
            'baz',
        ])
    """
    pkg_list = [pkg for pkg in pkg_list if not is_installed(pkg)]
    if pkg_list:
        install(pkg_list, update)


def nopackage(pkg_name):
    """
    Require a deb package to be uninstalled.

    Example::

        from fabtools import require

        require.deb.nopackage('apache2')
    """
    if is_installed(pkg_name):
        uninstall(pkg_name)


def nopackages(pkg_list):
    """
    Require several deb packages to be uninstalled.

    Example::

        from fabtools import require

        require.deb.nopackages([
            'perl',
            'php5',
            'ruby',
        ])
    """
    pkg_list = [pkg for pkg in pkg_list if is_installed(pkg)]
    if pkg_list:
        uninstall(pkg_list)
