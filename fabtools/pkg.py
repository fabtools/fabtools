"""
SmartOS packages
================

This module provides tools to manage SmartOS packages.

"""
from __future__ import with_statement

from fabric.api import hide, quiet, run, settings

from fabtools.files import is_file
from fabtools.utils import run_as_root


MANAGER = 'pkgin'


def update_index(force=False):
    """
    Update pkgin package definitions.
    """
    manager = MANAGER
    if force:
        with quiet():
            run_as_root("%(manager)s cl" % locals())
        run_as_root("%(manager)s -f up" % locals())
    else:
        run_as_root("%(manager)s up" % locals())


def upgrade(full=False):
    """
    Upgrade all packages.
    """
    manager = MANAGER
    cmds = {'pkgin': {False: 'ug', True: 'fug'}}
    cmd = cmds[manager][full]
    run_as_root("%(manager)s -y %(cmd)s" % locals())


def is_installed(pkg_name):
    """
    Check if a package is installed.
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = run("yes 'y' | pkgin list | awk '{print $1}' | egrep -qio \"^%(pkg_name)s\"" % locals())
        if res.succeeded:
            return True
        return False


def install(packages, update=False, yes=None, options=None):
    """
    Install one or more packages.

    If *update* is ``True``, the package definitions will be updated
    first, using :py:func:`~fabtools.pkg.update_index`.

    Extra *yes* may be passed to ``pkgin`` to validate license if necessary.

    Extra *options* may be passed to ``pkgin`` if necessary.

    Example::

        import fabtools

        # Update index, then verbosely install a single package
        fabtools.pkg.install('redis', update=True, options='-V',)

        # Install multiple packages
        fabtools.pkg.install([
            'unzip',
            'top'
        ])

    """
    manager = MANAGER
    if update:
        update_index()
    if options is None:
        options = []
    elif isinstance(options, str):
        options = [options]
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options.append("-y")
    options = " ".join(options)
    if isinstance(yes, str):
        run_as_root('yes %(yes)s | %(manager)s %(options)s in %(packages)s' % locals())
    else:
        run_as_root('%(manager)s %(options)s in %(packages)s' % locals())


def uninstall(packages, orphan=False, options=None):
    """
    Remove one or more packages.

    If *orphan* is ``True``, orphan dependencies will be
    removed from the system.

    Extra *options* may be passed to ``pkgin`` if necessary.
    """
    manager = MANAGER
    if options is None:
        options = []
    elif isinstance(options, str):
        options = [options]
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options.append("-y")
    options = " ".join(options)
    if orphan:
        run_as_root('%(manager)s -y ar' % locals())
    run_as_root('%(manager)s %(options)s remove %(packages)s' % locals())


def smartos_build():
    """
    Get the build of SmartOS. Useful to determine provider for example.

    Example::

        from fabtools.pkg import smartos_build

        if smartos_build().startswith('joyent'):
            print('SmartOS Joyent')

    """
    with settings(hide('running', 'stdout')):
        return run('uname -v')


def smartos_image():
    """
    Get the SmartOS image. Useful to determine the image/dataset for example.
    Returns None if it can't be determined.

    Example::

        from fabtools.pkg import smartos_image

        if smartos_image().startswith('percona'):
            sudo("mysql -uroot -psecretpassword -e 'show databases;'")

    """
    with settings(hide('running', 'stdout')):
        if is_file('/etc/product'):
            return run('cat /etc/product | head -n 2 | tail -n 1 | awk \'{ print $2 " " $3 }\'')
        else:
            return None
