"""
Conda environments and packages
================================

This module provides high-level tools for using conda environments.

"""

from fabtools.conda import (
    is_conda_installed,
    install_miniconda,
    create_env,
    env_exists,
    env,
    install,
    is_installed
)
from fabtools.system import UnsupportedFamily, distrib_family


def conda(prefix='~/miniconda', use_sudo=False):
    """
    Require conda to be installed.

    If conda is not installed the latest version of miniconda will be installed.

    :param prefix: prefix for the miniconda installation
    :param use_sudo: use sudo for this operation
    """
    if not is_conda_installed():
        install_miniconda(prefix=prefix, use_sudo=use_sudo)


def env(name=None, pkg_list=None, **kwargs):
    """
    Require a conda environment.
    If pkg_list is given, these are also required.

    :param name: name of environment
    :param pkg_list: list of required packages
    :param **kwargs: arguments to fabtools.conda.create_env()
    """

    conda()

    prefix = kwargs.get('prefix', None)
    if not env_exists(name=name, prefix=prefix):
        create_env(name=name, packages=pkg_list, **kwargs)
    else:
        packages(pkg_list, name=name, prefix=prefix, **kwargs)


def package(pkg_name, name=None, prefix=None, **kwargs):
    """
    Require a conda package.

    If the package is not installed, it will be installed using 'conda install'.
    """

    packages([pkg_name], name=name, prefix=prefix, **kwargs)


def packages(pkg_list, name=None, prefix=None, **kwargs):
    """
    Require several conda packages.

    """
    install(pkg_list, name=name, prefix=prefix, **kwargs)
