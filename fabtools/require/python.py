"""
Python environments and packages
================================

This module includes tools for using `virtual environments`_
and installing packages using `pip`_.

.. _virtual environments: http://www.virtualenv.org/
.. _pip: http://www.pip-installer.org/

"""

from fabtools.python import (
    create_virtualenv,
    install,
    install_pip,
    install_requirements,
    is_installed,
    is_pip_installed,
    virtualenv_exists,
)
from fabtools.python_setuptools import (
    install_setuptools,
    is_setuptools_installed,
)
from fabtools.system import distrib_family


MIN_SETUPTOOLS_VERSION = '0.7'
MIN_PIP_VERSION = '1.3.1'


def setuptools(version=MIN_SETUPTOOLS_VERSION, python_cmd='python'):
    """
    Require `setuptools`_ to be installed.

    If setuptools is not installed, or if a version older than *version*
    is installed, the latest version will be installed.

    .. _setuptools: http://pythonhosted.org/setuptools/
    """

    from fabtools.require.deb import packages as require_deb_packages
    from fabtools.require.rpm import packages as require_rpm_packages

    if not is_setuptools_installed(python_cmd=python_cmd):
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

        install_setuptools(python_cmd=python_cmd)


def pip(version=MIN_PIP_VERSION, pip_cmd='pip', python_cmd='python'):
    """
    Require `pip`_ to be installed.

    If pip is not installed, or if a version older than *version*
    is installed, the latest version will be installed.

    .. _pip: http://www.pip-installer.org/
    """
    setuptools(python_cmd=python_cmd)
    if not is_pip_installed(version, pip_cmd=pip_cmd):
        install_pip(python_cmd=python_cmd)


def package(pkg_name, url=None, pip_cmd='pip', python_cmd='python', **kwargs):
    """
    Require a Python package.

    If the package is not installed, it will be installed
    using the `pip installer`_.

    Package names are case insensitive.

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
    pip(MIN_PIP_VERSION, python_cmd=python_cmd)
    if not is_installed(pkg_name, pip_cmd=pip_cmd):
        install(url or pkg_name, pip_cmd=pip_cmd, **kwargs)


def packages(pkg_list, pip_cmd='pip', python_cmd='python', **kwargs):
    """
    Require several Python packages.

    Package names are case insensitive.
    """
    pip(MIN_PIP_VERSION, python_cmd=python_cmd)
    pkg_list = [pkg for pkg in pkg_list if not is_installed(pkg, pip_cmd=pip_cmd)]
    if pkg_list:
        install(pkg_list, pip_cmd=pip_cmd, **kwargs)


def requirements(filename, pip_cmd='pip', python_cmd='python', **kwargs):
    """
    Require Python packages from a pip `requirements file`_.

    .. _requirements file: http://www.pip-installer.org/en/latest/requirements.html
    """
    pip(MIN_PIP_VERSION, python_cmd=python_cmd)
    install_requirements(filename, pip_cmd=pip_cmd, **kwargs)


def virtualenv(directory, system_site_packages=False, venv_python=None,
               use_sudo=False, user=None, clear=False, prompt=None,
               virtualenv_cmd='virtualenv', pip_cmd='pip', python_cmd='python'):
    """
    Require a Python `virtual environment`_.

    ::

        from fabtools import require

        require.python.virtualenv('/path/to/venv')

    .. _virtual environment: http://www.virtualenv.org/
    """

    package('virtualenv', use_sudo=True, pip_cmd=pip_cmd, python_cmd=python_cmd)

    if not virtualenv_exists(directory):
        create_virtualenv(
            directory,
            system_site_packages=system_site_packages,
            venv_python=venv_python,
            use_sudo=use_sudo,
            user=user,
            clear=clear,
            prompt=prompt,
            virtualenv_cmd=virtualenv_cmd,
        )
