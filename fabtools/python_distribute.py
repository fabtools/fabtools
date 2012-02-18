"""
Fabric tools for managing Python packages using distribute
"""
from __future__ import with_statement

from fabric.api import *


def is_distribute_installed():
    """
    Check if distribute is installed
    """
    with settings(hide('running', 'warnings', 'stderr', 'stdout'), warn_only=True):
        res = run('easy_install --version')
        return res.succeeded and (res.find('distribute') >= 0)


def install_distribute():
    """
    Install distribute
    """
    with cd("/tmp"):
        run("curl --silent -O http://python-distribute.org/distribute_setup.py")
        sudo("python distribute_setup.py")


def install(packages, installer=None, upgrade=False, use_sudo=False):
    """
    Install Python packages with distribute
    """
    func = use_sudo and sudo or run
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options = []
    if upgrade:
        options.append("-U")
    options = " ".join(options)
    func('easy_install %(options)s %(packages)s' % locals())
