"""
Fabric tools for managing Debian/Ubuntu packages
"""
from fabric.api import *


def update_index():
    """
    Quietly update package index
    """
    sudo("aptitude -q -q update")


def upgrade():
    """
    Upgrade all packages
    """
    sudo("aptitude --assume-yes safe-upgrade")


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
    if update:
        update_index()
    if options is None:
        options = []
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options.append("--assume-yes")
    options = " ".join(options)
    sudo('aptitude install %(options)s %(packages)s' % locals())


def preseed_package(pkg_name, preseed):
    """
    Enable unattended package installation by preseeding debconf parameters
    """
    for q_name, _ in preseed.items():
        q_type, q_answer = _
        sudo('echo "%(pkg_name)s %(q_name)s %(q_type)s %(q_answer)s" | debconf-set-selections' % locals())
