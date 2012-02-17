"""
Idempotent API for managing Python packages
"""
import os.path

from fabtools.files import is_file
from fabtools.python import *
from fabtools.python_distribute import is_distribute_installed, install_distribute
from fabtools.require import deb


def distribute():
    """
    Require distribute
    """
    deb.packages([
        'curl',
        'python-dev',
    ])
    if not is_distribute_installed():
        install_distribute()


def pip(version=None):
    """
    Require pip
    """
    distribute()
    if not is_pip_installed(version):
        install_pip()


def package(pkg_name, url=None, use_sudo=False, user=None):
    """
    Require a Python package
    """
    pip('1.1')
    if not is_installed(pkg_name):
        install(url or pkg_name, use_sudo=use_sudo, user=user)


def packages(pkg_list, use_sudo=False, user=None):
    """
    Require several Python packages
    """
    pip('1.1')
    pkg_list = [pkg for pkg in pkg_list if not is_installed(pkg)]
    if pkg_list:
        install(pkg_list, use_sudo=use_sudo, user=user)


def requirements(filename, use_sudo=False, user=None):
    """
    Require Python packages from a pip requirements file
    """
    pip('1.1')
    install_requirements(filename, use_sudo=use_sudo, user=user)


def virtualenv(directory, system_site_packages=False, python=None, use_sudo=False, user=None):
    """
    Require a Python virtual environment
    """
    package('virtualenv', use_sudo=True)
    if not is_file(os.path.join(directory, 'bin', 'python')):
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
