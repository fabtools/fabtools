"""
Fabric tools for managing Debian/Ubuntu packages
"""
from __future__ import with_statement

from fabric.api import *


MANAGER = 'apt-get'


def update_index():
    """
    Quietly update package index
    """
    sudo("%s -q -q update" % MANAGER)


def upgrade(safe=True):
    """
    Upgrade all packages
    """
    manager = MANAGER
    cmds = {'apt-get': {False: 'dist-upgrade', True: 'upgrade'},
            'aptitude': {False: 'full-upgrade', True: 'safe-upgrade'}}
    cmd = cmds[manager][safe]
    sudo("%(manager)s --assume-yes %(cmd)s" % locals())


def is_installed(pkg_name):
    """
    Check if .deb package is installed
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = run("dpkg -s %(pkg_name)s" % locals())
        for line in res.splitlines():
            if line.startswith("Status: "):
                status = line[8:]
                if "installed" in status.split(' '):
                    return True
        return False


def install(packages, update=False, options=None):
    """
    Install .deb package(s)
    """
    manager = MANAGER
    if update:
        update_index()
    if options is None:
        options = []
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options.append("--assume-yes")
    options = " ".join(options)
    sudo('%(manager)s install %(options)s %(packages)s' % locals())


def uninstall(packages, purge=False, options=None):
    """
    Remove .deb package(s)
    """
    manager = MANAGER
    command = "purge" if purge else "remove"
    if options is None:
        options = []
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options.append("--assume-yes")
    options = " ".join(options)
    sudo('%(manager)s %(command)s %(options)s %(packages)s' % locals())


def preseed_package(pkg_name, preseed):
    """
    Enable unattended package installation by preseeding debconf parameters
    """
    for q_name, _ in preseed.items():
        q_type, q_answer = _
        sudo('echo "%(pkg_name)s %(q_name)s %(q_type)s %(q_answer)s" | debconf-set-selections' % locals())


def get_selections():
    """
    Get the state of dkpg selections
    Returns dict with state => [packages]
    """
    with settings(hide('stdout')):
        res = sudo('dpkg --get-selections')
    selections = dict()
    for line in res.splitlines():
        package, status = line.split()
        selections.setdefault(status, list()).append(package)
    return selections


def distrib_codename():
    """
    Get the codename of the distrib
    """
    with settings(hide('running', 'stdout')):
        return run('lsb_release --codename --short')
