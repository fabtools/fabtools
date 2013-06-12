"""
Python environments and packages
================================

This module includes tools for using `virtual environments`_
and installing packages using `pip`_.

.. _virtual environments: http://www.virtualenv.org/
.. _pip: http://www.pip-installer.org/

"""
import posixpath

from fabric.api import run, sudo

from fabtools.files import is_file
from fabtools.python import (
    install,
    install_pip,
    install_requirements,
    is_installed,
    is_pip_installed,
)
from fabtools.python_distribute import (
    install_distribute,
    is_distribute_installed,
)
from fabtools.system import distrib_family


DEFAULT_PIP_VERSION = '1.3.1'


def distribute(use_python='python'):
    """
    Require `distribute`_ to be installed.

    .. _distribute: http://packages.python.org/distribute/
    """

    from fabtools.require.deb import packages as require_deb_packages
    from fabtools.require.rpm import packages as require_rpm_packages

    family = distrib_family()

    if family == 'debian':
        require_deb_packages([
            'curl',
            'python-dev',
        ])

    elif family == 'redhat':

        require_rpm_packages([
            'curl',
            'python-devel',
        ])

    if not is_distribute_installed(use_python=use_python):
        install_distribute(use_python=use_python)


def pip(version=None, use_python='python'):
    """
    Require `pip`_ to be installed.
    """
    distribute(use_python=use_python)
    if not is_pip_installed(version, use_python=use_python):
        install_pip(use_python=use_python)


def package(pkg_name, url=None, use_python='python', **kwargs):
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
    pip(DEFAULT_PIP_VERSION, use_python=use_python)
    if not is_installed(pkg_name, use_python):
        install(url or pkg_name, use_python=use_python, **kwargs)


def packages(pkg_list, use_python='python', **kwargs):
    """
    Require several Python packages.
    """
    pip(DEFAULT_PIP_VERSION, use_python=use_python)
    pkg_list = [pkg for pkg in pkg_list if not is_installed(pkg, use_python=use_python)]
    if pkg_list:
        install(pkg_list, use_python=use_python, **kwargs)


def requirements(filename, use_python='python', **kwargs):
    """
    Require Python packages from a pip `requirements file`_.

    .. _requirements file: http://www.pip-installer.org/en/latest/requirements.html
    """
    pip(DEFAULT_PIP_VERSION, use_python=use_python)
    install_requirements(filename, use_python=use_python, **kwargs)


def virtualenv(directory, system_site_packages=False, python=None,
               use_sudo=False, user=None, clear=False,
               prompt=None, use_python='python'):
    """
    Require a Python `virtual environment`_.

    ::

        from fabtools import require

        require.python.virtualenv('/path/to/venv')

    .. _virtual environment: http://www.virtualenv.org/
    """
    package('virtualenv', use_sudo=True, use_python=use_python)
    if not is_file(posixpath.join(directory, 'bin', 'python')):
        options = ['--quiet']
        if system_site_packages:
            options.append('--system-site-packages')
        if python:
            options.append('--python=%s' % python)
        if clear:
            options.append('--clear')
        if prompt:
            options.append('--prompt="%s"' % prompt)
        options = ' '.join(options)
        command = 'virtualenv %(options)s "%(directory)s"' % locals()
        if use_sudo:
            sudo(command, user=user)
        else:
            run(command)
