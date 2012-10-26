"""
Python environments and packages
================================

This module includes tools for using `virtual environments`_
and installing packages using `pip`_.

.. _virtual environments: http://www.virtualenv.org/
.. _pip: http://www.pip-installer.org/

"""
import posixpath

from fabtools.files import is_file
from fabtools.python import *
from fabtools.python_distribute import is_distribute_installed, install_distribute
from fabtools.require import deb


DEFAULT_PIP_VERSION = '1.2.1'


def distribute():
    """
    Require `distribute`_ to be installed.

    .. _distribute: http://packages.python.org/distribute/
    """
    deb.packages([
        'curl',
        'python-dev',
    ])
    if not is_distribute_installed():
        install_distribute()


def pip(version=None):
    """
    Require `pip`_ to be installed.
    """
    distribute()
    if not is_pip_installed(version):
        install_pip()


def package(pkg_name, url=None, **kwargs):
    """
    Require a Python package.

    If the package is not installed, it will be installed
    using the `pip installer`_.

    ::

        from fabtools.python import virtualenv
        from fabtools import require

        # Install package system-wide
        require.python.package('foo', use_sudo=True)

        # Install package in an existing virtual environment
        with virtualenv('/path/to/venv'):
            require.python.package('bar')

    .. _pip installer: http://www.pip-installer.org/
    """
    pip(DEFAULT_PIP_VERSION)
    if not is_installed(pkg_name):
        install(url or pkg_name, **kwargs)


def packages(pkg_list, **kwargs):
    """
    Require several Python packages.
    """
    pip(DEFAULT_PIP_VERSION)
    pkg_list = [pkg for pkg in pkg_list if not is_installed(pkg)]
    if pkg_list:
        install(pkg_list, **kwargs)


def requirements(filename, **kwargs):
    """
    Require Python packages from a pip `requirements file`_.

    .. _requirements file: http://www.pip-installer.org/en/latest/requirements.html
    """
    pip(DEFAULT_PIP_VERSION)
    install_requirements(filename, **kwargs)


def virtualenv(directory, system_site_packages=False, python=None, use_sudo=False, user=None):
    """
    Require a Python `virtual environment`_.

    ::

        from fabtools import require

        require.python.virtualenv('/path/to/venv')

    .. _virtual environment: http://www.virtualenv.org/
    """
    package('virtualenv', use_sudo=True)
    if not is_file(posixpath.join(directory, 'bin', 'python')):
        options = ['--quiet']
        if system_site_packages:
            options.append('--system-site-packages')
        if python:
            options.append('--python=%s' % python)
        options = ' '.join(options)
        command = 'virtualenv %(options)s "%(directory)s"' % locals()
        if use_sudo:
            sudo(command, user=user)
        else:
            run(command)
