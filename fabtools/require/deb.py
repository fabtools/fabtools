"""
Idempotent API for managing Debian/Ubuntu packages
"""
from __future__ import with_statement

from fabric.utils import puts

from fabtools.files import is_file, watch
from fabtools.deb import *
import fabtools.require


def source(name, uri, distribution, *components):
    """
    Require a package source
    """
    path = '/etc/apt/sources.list.d/%(name)s.list' % locals()
    components = ' '.join(components)
    source_line = 'deb %(uri)s %(distribution)s %(components)s\n' % locals()
    def on_update():
        puts('Added APT repository: %s' % source_line)
        update_index()
    with watch(path, _callable=on_update):
        fabtools.require.file(path=path, contents=source_line, use_sudo=True)


def ppa(name):
    """
    Require a PPA
    """
    assert name.startswith('ppa:')
    user, repo = name[4:].split('/', 2)
    distrib = distrib_codename()
    source = '%(user)s-%(repo)s-%(distrib)s.list' % locals()

    if not is_file(source):
        package('python-software-properties')
        sudo('add-apt-repository %s' % name)
        update_index()


def package(pkg_name, update=False):
    """
    Require a deb package
    """
    if not is_installed(pkg_name):
        install(pkg_name, update)


def packages(pkg_list, update=False):
    """
    Require several deb packages
    """
    pkg_list = [pkg for pkg in pkg_list if not is_installed(pkg)]
    if pkg_list:
        install(pkg_list, update)


def nopackage(pkg_name):
    """
    Require a deb package to be absent
    """
    if is_installed(pkg_name):
        uninstall(pkg_name)


def nopackages(pkg_list):
    """
    Require several deb packages to be absent
    """
    pkg_list = [pkg for pkg in pkg_list if is_installed(pkg)]
    if pkg_list:
        uninstall(pkg_list)
