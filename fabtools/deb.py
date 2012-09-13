"""
Debian packages
===============

This module provides tools to manage Debian/Ubuntu packages
and repositories.

"""
from __future__ import with_statement

from fabric.api import *


MANAGER = 'apt-get'


def update_index(quiet=True):
    """
    Update APT package definitions.
    """
    options = "-q -q" if quiet else ""
    sudo("%s %s update" % (MANAGER, options))


def upgrade(safe=True):
    """
    Upgrade all packages.
    """
    manager = MANAGER
    cmds = {'apt-get': {False: 'dist-upgrade', True: 'upgrade'},
            'aptitude': {False: 'full-upgrade', True: 'safe-upgrade'}}
    cmd = cmds[manager][safe]
    sudo("%(manager)s --assume-yes %(cmd)s" % locals())


def is_installed(pkg_name):
    """
    Check if a package is installed.
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
    Install one or more packages.

    If *update* is ``True``, the package definitions will be updated
    first, using :py:func:`~fabtools.deb.update_index`.

    Extra *options* may be passed to ``apt-get`` if necessary.

    Example::

        import fabtools

        # Update index, then install a single package
        fabtools.deb.install('build-essential', update=True)

        # Install multiple packages
        fabtools.deb.install([
            'python-dev',
            'libxml2-dev',
        ])

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
    Remove one or more packages.

    If *purge* is ``True``, the package configuration files will be
    removed from the system.

    Extra *options* may be passed to ``apt-get`` if necessary.
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
    Enable unattended package installation by preseeding ``debconf``
    parameters.

    Example::

        import fabtools

        # Unattended install of Postfix mail server
        fabtools.deb.preseed_package('postfix', {
            'postfix/main_mailer_type': ('select', 'Internet Site'),
            'postfix/mailname': ('string', 'example.com'),
            'postfix/destinations': ('string', 'example.com, localhost.localdomain, localhost'),
        })
        fabtools.deb.install('postfix')

    """
    for q_name, _ in preseed.items():
        q_type, q_answer = _
        sudo('echo "%(pkg_name)s %(q_name)s %(q_type)s %(q_answer)s" | debconf-set-selections' % locals())


def get_selections():
    """
    Get the state of ``dkpg`` selections.

    Returns a dict with state => [packages].
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
    Get the codename of the distrib.

    Example::

        from fabtools.deb import distrib_codename

        if distrib_codename() == 'precise':
            print('Ubuntu 12.04 LTS')

    """
    with settings(hide('running', 'stdout')):
        return run('lsb_release --codename --short')


def add_apt_key(filename, update=True):
    """
    Trust packages signed with this public key.

    Example::

        import fabtools

        # Download 3rd party APT public key
        if not fabtools.is_file('rabbitmq-signing-key-public.asc'):
            run('wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc')

        # Tell APT to trust that key
        fabtools.deb.add_apt_key('rabbitmq-signing-key-public.asc')

    """
    sudo('apt-key add %(filename)s' % locals())
    if update:
        update_index()
