"""
RPM packages
============

This module provides high-level tools for managing CentOS/RHEL/SL/Fedora
packages and repositories.

"""

from fabric.api import hide, settings
from fabtools.rpm import (
    install,
    is_installed,
    uninstall,
)
from fabtools.system import get_arch, distrib_release
from fabtools.utils import run_as_root


def package(pkg_name, repos=None, yes=None, options=None):
    """
    Require an RPM package to be installed.

    Example::

        from fabtools import require

        require.rpm.package('emacs')
    """
    if not is_installed(pkg_name):
        install(pkg_name, repos, yes, options)


def packages(pkg_list, repos=None, yes=None, options=None):
    """
    Require several RPM packages to be installed.

    Example::

        from fabtools import require

        require.rpm.packages([
            'nano',
            'unzip',
            'vim',
        ])
    """
    pkg_list = [pkg for pkg in pkg_list if not is_installed(pkg)]
    if pkg_list:
        install(pkg_list, repos, yes, options)


def nopackage(pkg_name, options=None):
    """
    Require an RPM package to be uninstalled.

    Example::

        from fabtools import require

        require.rpm.nopackage('emacs')
    """
    if is_installed(pkg_name):
        uninstall(pkg_name, options)


def nopackages(pkg_list, options=None):
    """
    Require several RPM packages to be uninstalled.

    Example::

        from fabtools import require

        require.rpm.nopackages([
            'unzip',
            'vim',
            'emacs',
        ])
    """
    pkg_list = [pkg for pkg in pkg_list if is_installed(pkg)]
    if pkg_list:
        uninstall(pkg_list, options)


def repository(name):
    """
    Require a repository. Aimed for 3rd party repositories.

    *Name* currently only supports EPEL and RPMforge.

    Example::

        from fabtools import require

        # RPMforge packages for CentOS 6
        require.rpm.repository('rpmforge')


    """
    name = name.lower()
    epel_url = 'http://download.fedoraproject.org/pub/epel'
    rpmforge_url = 'http://packages.sw.be/rpmforge-release/rpmforge-release'
    rpmforge_version = '0.5.2-2'
    arch = get_arch()
    try:
        release = int(str(distrib_release()))
    except ValueError:
        release = int(float(str(distrib_release())))
    if release == 6:
        epel_version = '6-8'
    elif release == 5:
        epel_version = '5-4'
    if name == 'rpmforge' and arch == 'i386':
        arch = 'i686'
    supported = {
        'rpmforge': {
            '%(arch)s' % locals(): {
                '6': '%(rpmforge_url)s-%(rpmforge_version)s.el6.rf.i686.rpm' % locals(),
                '5': '%(rpmforge_url)s-%(rpmforge_version)s.el5.rf.x86_64.rpm' % locals(),
            },
        },
        'epel': {
            '%(arch)s' % locals(): {
                '6': '%(epel_url)s/6/%(arch)s/epel-release-%(epel_version)s.noarch.rpm' % locals(),
                '5': '%(epel_url)s/5/%(arch)s/epel-release-%(epel_version)s.noarch.rpm' % locals(),
            }
        },
    }
    keys = {
        'rpmforge': 'http://apt.sw.be/RPM-GPG-KEY.dag.txt',
        'epel': '%(epel_url)s/RPM-GPG-KEY-EPEL-%(release)s' % locals(),
    }
    repo = supported[name][str(arch)][str(release)]
    key = keys[name]
    with settings(hide('warnings'), warn_only=True):
        run_as_root('rpm --import %(key)s' % locals())
        run_as_root('rpm -Uh %(repo)s' % locals())
