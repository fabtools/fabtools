"""
Fabric tools for managing Python packages using pip
"""
from __future__ import with_statement

from contextlib import contextmanager
from distutils.version import StrictVersion as V
import os.path

from fabric.api import *
from fabric.utils import puts


def is_pip_installed(version=None):
    """
    Check if pip is installed
    """
    with settings(hide('running', 'warnings', 'stderr', 'stdout'), warn_only=True):
        res = run('pip --version')
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
    Install pip
    """
    with cd("/tmp"):
        run("curl --silent -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py")
        sudo("python get-pip.py")


def is_installed(package):
    """
    Check if a Python package is installed
    """
    options = []
    options = " ".join(options)
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = run("pip freeze %(options)s" % locals())
    packages = [line.split('==')[0] for line in res.splitlines()]
    return (package in packages)


def install(packages, upgrade=False, use_mirrors=True, use_sudo=False, user=None):
    """
    Install Python packages
    """
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options = []
    if use_mirrors:
        options.append('--use-mirrors')
    if upgrade:
        options.append("--upgrade")
    options = " ".join(options)
    command =  'pip install %(options)s %(packages)s' % locals()
    if use_sudo:
        sudo(command, user=user)
    else:
        run(command)


def install_requirements(filename, upgrade=False, use_mirrors=True, use_sudo=False, user=None):
    """
    Install Python packages from a pip requirements file
    """
    options = []
    if use_mirrors:
        options.append('--use-mirrors')
    if upgrade:
        options.append("--upgrade")
    options = " ".join(options)
    command = 'pip install %(options)s -r %(filename)s' % locals()
    if use_sudo:
        sudo(command, user=user)
    else:
        run(command)


@contextmanager
def virtualenv(directory):
    """
    Context manager to activate a Python virtualenv
    """
    with cd(directory):
        with prefix('source "%s"' % os.path.join(directory, 'bin', 'activate')):
            yield
