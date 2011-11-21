"""
Idempotent API for managing Debian/Ubuntu packages
"""
from fabtools.files import is_file
from fabtools.deb import *


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
