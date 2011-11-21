"""
Idempotent API for managing python packages
"""
import os.path

from fabtools.files import is_file
from fabtools.python import *
from fabtools.python_distribute import is_distribute_installed, install_distribute
from fabtools.icanhaz import deb


def distribute():
    """
    I can haz distribute
    """
    deb.packages([
        'curl',
        'python-dev',
    ])
    if not is_distribute_installed():
        install_distribute()


def pip(version=None):
    """
    I can haz pip
    """
    distribute()
    if not is_pip_installed(version):
        install_pip()


def package(pkg_name, url=None, virtualenv=None, use_sudo=False, user=None):
    """
    I can haz python package
    """
    pip("1.0.2")
    if not is_installed(pkg_name):
        install(url or pkg_name, virtualenv=virtualenv, use_sudo=use_sudo, user=user)


def packages(pkg_list, virtualenv=None, use_sudo=False, user=None):
    """
    I can haz python packages
    """
    pip("1.0.2")
    pkg_list = [pkg for pkg in pkg_list if not is_installed(pkg)]
    if pkg_list:
        install(pkg_list, virtualenv=virtualenv, use_sudo=use_sudo, user=user)


def requirements(filename, virtualenv=None, use_sudo=False, user=None):
    """
    I can haz python packages from a pip requirements file
    """
    pip("1.0.2")
    install_requirements(filename, virtualenv=virtualenv, use_sudo=use_sudo, user=user)


def virtualenv(directory, no_site_packages=True, python=None, use_sudo=False, user=None):
    """
    I can haz python virtual environment
    """
    package('virtualenv', use_sudo=True)
    if not is_file(os.path.join(directory, 'bin', 'python')):
        options = ['--quiet']
        if no_site_packages:
            options.append('--no-site-packages')
        if python:
            options.append('--python=%s' % python)
        options = ' '.join(options)
        command = 'virtualenv %(options)s "%(directory)s"' % locals()
        if use_sudo:
            sudo(command, user=user)
        else:
            run(command)
