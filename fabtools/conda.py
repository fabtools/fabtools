"""
Conda packages
===============

This module provides tools for installing conda packages using
the `miniconda`_ distribution.

.. _miniconda: http://conda.pydata.org/miniconda.html

"""

from fabric.api import cd, run, settings, hide
from fabric.contrib import files

from fabtools.utils import download, run_as_root


MINICONDA_URL = 'http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh'

def install_miniconda(python_cmd='python', use_sudo=True, prefix='~/miniconda'):
    """
    Install the latest version of `miniconda`_.

    :param prefix: prefix for the miniconda installation

    ::

        import fabtools

        fabtools.conda.install_miniconda()

    """

    with cd("/tmp"):
        download(MINICONDA_URL)

        command = 'bash Miniconda-latest-Linux-x86_64.sh -b -p %(prefix)s' % locals()
        if use_sudo:
            run_as_root(command)
        else:
            run(command)
        files.append('~/.bash_profile', 'export PATH=%(prefix)s/bin:$PATH' % locals())

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
