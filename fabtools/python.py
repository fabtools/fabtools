"""
Python environments and packages
================================

This module includes tools for using `virtual environments`_
and installing packages using `pip`_.

.. _virtual environments: http://www.virtualenv.org/
.. _pip: http://www.pip-installer.org/

"""
from __future__ import with_statement

from contextlib import contextmanager
from distutils.version import StrictVersion as V
from pipes import quote
import os
import posixpath

from fabric.api import cd, hide, prefix, run, settings, sudo
from fabric.utils import puts

from fabtools.utils import abspath, run_as_root


def is_pip_installed(version=None):
    """
    Check if `pip`_ is installed.

    .. _pip: http://www.pip-installer.org/
    """
    with settings(hide('running', 'warnings', 'stderr', 'stdout'), warn_only=True):
        res = run('pip --version 2>/dev/null')
        if res.failed:
            return False
        if version is None:
            return res.succeeded
        else:
            installed = res.split(' ')[1]
            if V(installed) < V(version):
                puts("pip %s found (version >= %s required)" % (installed, version))
                return False
            else:
                return True


def install_pip():
    """
    Install the latest version of `pip`_.

    .. _pip: http://www.pip-installer.org/

    ::

        import fabtools

        if not fabtools.python.is_pip_installed():
            fabtools.python.install_pip()

    """
    with cd('/tmp'):
        run('curl --silent -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py')
        run_as_root('python get-pip.py', pty=False)


def is_installed(package):
    """
    Check if a Python package is installed.
    """
    options = []
    options = ' '.join(options)
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = run('pip freeze %(options)s' % locals())
    packages = [line.split('==')[0] for line in res.splitlines()]
    return (package in packages)


def install(packages, upgrade=False, use_mirrors=True, use_sudo=False,
            user=None, download_cache=None, quiet=False):
    """
    Install Python package(s) using `pip`_.

    .. _pip: http://www.pip-installer.org/

    Examples::

        import fabtools

        # Install a single package
        fabtools.python.install('package', use_sudo=True)

        # Install a list of packages
        fabtools.python.install(['pkg1', 'pkg2'], use_sudo=True)

    """
    if not isinstance(packages, basestring):
        packages = ' '.join(packages)
    options = []
    if use_mirrors:
        options.append('--use-mirrors')
    if upgrade:
        options.append('--upgrade')
    if download_cache:
        options.append('--download-cache="%s"' % download_cache)
    if quiet:
        options.append('--quiet')
    options = ' '.join(options)
    command = 'pip install %(options)s %(packages)s' % locals()
    if use_sudo:
        sudo(command, user=user, pty=False)
    else:
        run(command, pty=False)


def install_requirements(filename, upgrade=False, use_mirrors=True,
                         use_sudo=False, user=None, download_cache=None,
                         quiet=False):
    """
    Install Python packages from a pip `requirements file`_.

    ::

        import fabtools

        fabtools.python.install_requirements('project/requirements.txt')

    .. _requirements file: http://www.pip-installer.org/en/latest/requirements.html
    """
    options = []
    if use_mirrors:
        options.append('--use-mirrors')
    if upgrade:
        options.append('--upgrade')
    if download_cache:
        options.append('--download-cache="%s"' % download_cache)
    if quiet:
        options.append('--quiet')
    options = ' '.join(options)
    command = 'pip install %(options)s -r %(filename)s' % locals()
    if use_sudo:
        sudo(command, user=user, pty=False)
    else:
        run(command, pty=False)


@contextmanager
def virtualenv(directory, local=False):
    """
    Context manager to activate an existing Python `virtual environment`_.

    ::

        from fabric.api import run
        from fabtools.python import virtualenv

        with virtualenv('/path/to/virtualenv'):
            run('python -V')

    .. _virtual environment: http://www.virtualenv.org/
    """

    path_mod = os.path if local else posixpath

    # Build absolute path to the virtualenv activation script
    venv_path = abspath(directory)
    activate_path = path_mod.join(venv_path, 'bin', 'activate')

    # Source the activation script
    with prefix('. %s' % quote(activate_path)):
        yield
