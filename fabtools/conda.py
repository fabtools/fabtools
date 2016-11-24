"""
Conda packages
===============

This module provides tools for installing conda packages using
the `miniconda`_ distribution.

.. _miniconda: http://conda.pydata.org/miniconda.html

"""
from contextlib import contextmanager
from pipes import quote
import os
import posixpath

from fabric.api import cd, run, settings, hide, prefix
from fabric.contrib import files
from fabric.operations import sudo
from fabtools import utils
import fabtools

from fabtools.utils import download, run_as_root

MINICONDA_URL = 'http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh'

def install_miniconda(prefix='~/miniconda', use_sudo=False, keep_installer=False):
    """
    Install the latest version of `miniconda`_.

    :param prefix: prefix for the miniconda installation
    :param use_sudo: use sudo for this operation
    :param keep_installer: keep the miniconda installer after installing

    ::

        import fabtools

        fabtools.conda.install_miniconda()

    """

    with cd("/tmp"):
        if not fabtools.files.is_file('Miniconda-latest-Linux-x86_64.sh'):
            download(MINICONDA_URL)

        command = 'bash Miniconda-latest-Linux-x86_64.sh -b -p %(prefix)s' % locals()
        if use_sudo:
            run_as_root(command)
        else:
            run(command)
        files.append('~/.bash_profile', 'export PATH=%(prefix)s/bin:$PATH' % locals())

        if not keep_installer:
            run('rm -f Miniconda-latest-Linux-x86_64.sh')

def is_conda_installed():
    """
    Check if `conda` is installed.

    """
    with settings(hide('running', 'warnings', 'stderr', 'stdout'), warn_only=True):
        res = run('conda -V 2>/dev/null')
        if res.failed:
            return False
        return res.succeeded


def get_sysprefix():
    """
    Return the path of the conda installation.

    """

    return run("conda info -s | grep -e 'sys.prefix' | awk '{print $2}'")


def create_env(name=None, prefix=None, yes=True, override_channels=False,
               channels=None, packages=None, quiet=True, use_sudo=False,
               user=None):
    """
    Create a conda environment.

    :param name: name of environment (in conda environment directory)
    :param prefix: full path to environment prefix
    :param yes: do not ask for confirmation
    :param quiet: do not display progress bar
    :param override_channels: Do not search default or .condarc channels. Requires `channels` .True or False
    :param channels: additional channel to search for packages. These are
                        URLs searched in the order they are given (including
                        file:// for local directories). Then, the defaults or
                        channels from .condarc are searched (unless
                        `override-channels` is given). You can use 'defaults'
                        to get the default packages for conda, and 'system' to
                        get the system packages, which also takes .condarc
                        into account. You can also use any name and the
                        .condarc channel_alias value will be prepended. The
                        default channel_alias is http://conda.binstar.org/
    :param packages: package versions to install into conda environment
    :param use_sudo: Use sudo
    :param user: sudo user
    ::

        import fabtools

        fabtools.conda.create_(path='/path/to/venv')
    """
    options = []
    if override_channels:
        options.append('--override_channels')
    if name:
        options.append('--name ' + quote(name))
    if prefix:
        options.append('--prefix ' + quote(utils.abspath(prefix)))
    if yes:
        options.append('--yes')
    if quiet:
        options.append('--quiet')
    for ch in channels or []:
        options.append('-c ' + quote(ch))
    options.extend(packages or ['python'])

    options = ' '.join(options)


    command = 'conda create ' + options
    if use_sudo:
        sudo(command, user=user)
    else:
        run(command)


def env_exists(name=None, prefix=None):
    """
    Check if a conda environment exists.
    """
    if not prefix:  # search in default env dir
        command = "conda info -e | grep -e '^%(name)s\s'" % locals()
    else:
        # check if just a prefix or prefix & name are given:
        if name:
            base = prefix
        else:
            # we were given a full path to the environment.
            # we split this up into the parent directory + the environment path
            # so we can call 'conda info' with CONDA_ENVS_PATH set to the
            # parent dir
            prefix = utils.abspath(prefix)
            base, name = prefix, ''
            while name == '':
                base, name = os.path.split(base)
        command = "CONDA_ENVS_PATH=%(base)s conda info -e | grep -e '^%(name)s\s'" % locals()
    with settings(hide('running', 'warnings', 'stderr', 'stdout'), warn_only=True):
        res = run(command, shell_escape=False)
        return res.succeeded


@contextmanager
def env(envname):
    """
    Context manager to activate an existing conda environment.

    :param envname: name or path of the conda environment
    ::

        from fabric.api import run
        from fabtools.conda import env

        with env('envname'):
            run('python -V')
    """

    # Source the activation script
    with prefix('source activate ' + envname):
        yield

def install(packages=None, yes=True, force=False, file=None, unknown=False,
            channels=None, override_channels=False, name=None, prefix=None,
            quiet=True):
    """
    Install conda package(s).

    :param packages: package versions to install into conda environment
    :param yes: do not ask for confirmation
    :param force: force install (even when package already installed),
        implies --no-deps
    :param file: read package versions from FILE
    :param unknown: use index metadata from the local package cache (which
        are from unknown channels)
    :param channels: additional channel to search for packages. These are
        URLs searched in the order they are given (including
        file:// for local directories). Then, the defaults or
        channels from .condarc are searched (unless
        `override-channels` is given). You can use 'defaults'
        to get the default packages for conda, and 'system' to
        get the system packages, which also takes .condarc
        into account. You can also use any name and the
        .condarc channel_alias value will be prepended. The
        default channel_alias is http://conda.binstar.org/
    :param override_channels: Do not search default or .condarc channels.
        Requires `channels` .True or False
    :param name: name of environment (in conda environment directory)
    :param prefix: full path to environment prefix
    :param quiet: do not display progress bar
    """

    if isinstance(packages, basestring):
        packages = [packages]

    options = []
    if override_channels:
        options.append('--override_channels')
    if name:
        options.append('--name ' + quote(name))
    if prefix:
        options.append('--prefix ' + quote(utils.abspath(prefix)))
    if yes:
        options.append('--yes')
    if quiet:
        options.append('--quiet')
    if force:
        options.append('--force')
    if unknown:
        options.append('--unknown')
    if file:
        options.append('--file ' + quote(file))
    for ch in channels or []:
        options.append('-c ' + quote(ch))
    options.extend(packages or ['python'])

    options = ' '.join(options)

    command = 'conda install ' + options
    run(command)


def is_installed(package, name=None, prefix=None):
    """
    Check if a conda package is installed.

    :param name: name of environment (in conda environment directory)
    :param prefix: full path to environment prefix
    """
    options = []
    if name:
        options.append('--name ' + quote(name))
    if prefix:
        options.append('--prefix ' + quote(utils.abspath(prefix)))

    options = ' '.join(options)

    command = 'conda list %(options)s | grep -q %(package)s' % locals()
    with settings(hide('running', 'warnings', 'stderr', 'stdout'), warn_only=True):
        res = run(command)
    return res.succeeded