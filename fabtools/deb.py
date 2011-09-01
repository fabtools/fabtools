"""
Fabric tools for managing Debian/Ubuntu packages
"""
from fabric.api import *


def is_installed(pkg_name):
    """
    Check if .deb package is installed
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = run("dpkg -s %(pkg_name)s" % locals())
        return res.succeeded


def install_package(pkg_name, update=False):
    """
    Install .deb package
    """
    if update:
        sudo("aptitude -q -q update")   # quietly update package list
    options = "--assume-yes"
    sudo('aptitude install %(options)s %(pkg_name)s' % locals())


def install_packages(pkg_list, update=False):
    """
    Install several .deb packages
    """
    if update:
        sudo("aptitude -q -q update")   # quietly update package list
    pkg_names = ' '.join(pkg_list)
    options = "--assume-yes"
    sudo('aptitude install %(options)s %(pkg_names)s' % locals())


def preseed_package(pkg_name, preseed):
    """
    Enable unattended package installation by preseeding debconf parameters
    """
    for q_name, _ in preseed.items():
        q_type, q_answer = _
        sudo('echo "%(pkg_name)s %(q_name)s %(q_type)s %(q_answer)s" | debconf-set-selections' % locals())
