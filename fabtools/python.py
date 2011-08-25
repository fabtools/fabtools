"""
Fabric tools for managing Python packages
"""
from fabric.api import *


def install_packages(pkg_list, installer=None, upgrade=False, use_sudo=False):
    """
    Install Python packages

    Packages can be installed with pip or easy_install (setuptools/distribute)
    """
    func = use_sudo and sudo or run
    opts = []

    # Use pip if possible, or easy_install
    if installer is None:
        with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
            if func('pip -h').succeeded:
                installer = 'pip'
            elif func('easy_install -h').succeeded:
                installer = 'easy_install'
            else:
                abort("You need 'pip' or 'easy_install' (setuptools/distribute) to install Python packages")

    if installer == 'pip':
        opts += "--use-mirrors"
        if upgrade:
            opts += "-U"
        for pkg in pkg_list:
            func('pip install %s%s' % (' '.join(opts), pkg))

    elif installer == 'easy_install':
        if upgrade:
            opts += "-U"
        for pkg in pkg_list:
            func('easy_install %s%s' % (' '.join(opts), pkg))
