"""
Idempotent API for managing python packages
"""
from fabtools.python import *
from fabtools.python_distribute import is_distribute_installed, install_distribute
from fabtools.icanhaz import deb


def distribute():
    """
    I can haz distribute
    """
    deb.package('curl')
    if not is_distribute_installed():
        install_distribute()


def pip():
    """
    I can haz pip
    """
    distribute()
    if not is_pip_installed():
        install_pip()


def package(pkg_name, virtualenv=None, use_sudo=False):
    """
    I can haz python package
    """
    pip()
    if not is_installed(pkg_name):
        install(pkg_name, virtualenv, use_sudo)


def packages(pkg_list, virtualenv=None, use_sudo=False):
    """
    I can haz python packages
    """
    pip()
    pkg_list = [pkg for pkg in pkg_list if not is_installed(pkg)]
    if pkg_list:
        install(pkg_list, virtualenv, use_sudo)
