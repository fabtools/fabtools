"""
Python environments and packages
================================

This module provides high-level tools for using Python `virtual environments`_
and installing Python packages using the `pip`_ installer.

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
from fabtools.system import UnsupportedFamily, distrib_family


MIN_SETUPTOOLS_VERSION = '0.7'
MIN_PIP_VERSION = '1.5'


def setuptools(version=MIN_SETUPTOOLS_VERSION, python_cmd='python'):
    """
    Require `setuptools`_ to be installed.

    If setuptools is not installed, or if a version older than *version*
    is installed, the latest version will be installed.

    .. _setuptools: http://pythonhosted.org/setuptools/
    """

    from fabtools.require.deb import package as require_deb_package
    from fabtools.require.rpm import package as require_rpm_package

    if not is_setuptools_installed(python_cmd=python_cmd):
        family = distrib_family()

        if family == 'debian':
            require_deb_package('python-dev')
        elif family == 'redhat':
            require_rpm_package('python-devel')
        elif family == 'arch':
            pass  # ArchLinux installs header with base package
        else:
            raise UnsupportedFamily(supported=['debian', 'redhat', 'arch'])

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


def package(pkg_name, url=None, pip_cmd='pip', python_cmd='python',
            allow_external=False, allow_unverified=False, **kwargs):
    """
    Require a Python package.

    If the package is not installed, it will be installed
    using the `pip installer`_.

    Package names are case insensitive.

    Starting with version 1.5, pip no longer scrapes insecure external
    urls by default and no longer installs externally hosted files by
    default. Use ``allow_external=True`` or ``allow_unverified=True``
    to change these behaviours.

    ::

        from fabtools.python import virtualenv
        from fabtools import require

        # Install package system-wide (not recommended)
        require.python.package('foo', use_sudo=True)

        # Install package in an existing virtual environment
        with virtualenv('/path/to/venv'):
            require.python.package('bar')

    .. _pip installer: http://www.pip-installer.org/
    """
    pip(MIN_PIP_VERSION, python_cmd=python_cmd)
    if not is_installed(pkg_name, pip_cmd=pip_cmd):
        install(url or pkg_name,
                pip_cmd=pip_cmd,
                allow_external=[url or pkg_name] if allow_external else [],
                allow_unverified=[url or pkg_name] if allow_unverified else [],
                **kwargs)


def packages(pkg_list, pip_cmd='pip', python_cmd='python',
             allow_external=None, allow_unverified=None, **kwargs):
    """
    Require several Python packages.

    Package names are case insensitive.

    Starting with version 1.5, pip no longer scrapes insecure external
    urls by default and no longer installs externally hosted files by
    default. Use ``allow_external=['foo', 'bar']`` or
    ``allow_unverified=['bar', 'baz']`` to change these behaviours
    for specific packages.
    """
    if allow_external is None:
        allow_external = []

    if allow_unverified is None:
        allow_unverified = []

    pip(MIN_PIP_VERSION, python_cmd=python_cmd)

    pkg_list = [
        pkg for pkg in pkg_list if not is_installed(pkg, pip_cmd=pip_cmd)]
    if pkg_list:
        install(pkg_list,
                pip_cmd=pip_cmd,
                allow_external=allow_external,
                allow_unverified=allow_unverified,
                **kwargs)


def requirements(filename, pip_cmd='pip', python_cmd='python',
                 allow_external=None, allow_unverified=None, **kwargs):
    """
    Require Python packages from a pip `requirements file`_.

    Starting with version 1.5, pip no longer scrapes insecure external
    urls by default and no longer installs externally hosted files by
    default. Use ``allow_external=['foo', 'bar']`` or
    ``allow_unverified=['bar', 'baz']`` to change these behaviours
    for specific packages.

    ::

        from fabtools.python import virtualenv
        from fabtools import require

        # Install requirements in an existing virtual environment
        with virtualenv('/path/to/venv'):
            require.python.requirements('requirements.txt')

    .. _requirements file: http://www.pip-installer.org/en/latest/requirements.html
    """
    pip(MIN_PIP_VERSION, python_cmd=python_cmd)
    install_requirements(filename, pip_cmd=pip_cmd,
                         allow_external=allow_external,
                         allow_unverified=allow_unverified, **kwargs)


def virtualenv(directory, system_site_packages=False, venv_python=None,
               use_sudo=False, user=None, clear=False, prompt=None,
               virtualenv_cmd='virtualenv', pip_cmd='pip',
               python_cmd='python'):
    """
    Require a Python `virtual environment`_.

    ::

        from fabtools import require

        require.python.virtualenv('/path/to/venv')

    .. _virtual environment: http://www.virtualenv.org/
    """

    package('virtualenv', use_sudo=True, pip_cmd=pip_cmd,
            python_cmd=python_cmd)

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
