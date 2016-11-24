"""
RPM packages
============

This module provides tools to manage CentOS/RHEL/SL/Fedora packages
and repositories.

"""

from fabric.api import hide, run, settings

from fabtools.utils import run_as_root


MANAGER = 'yum -y --color=never'


def update(kernel=False):
    """
    Upgrade all packages, skip obsoletes if ``obsoletes=0`` in ``yum.conf``.

    Exclude *kernel* upgrades by default.
    """
    manager = MANAGER
    cmds = {
        'yum -y --color=never': {
            False: '--exclude=kernel* update', True: 'update'
        }
    }
    cmd = cmds[manager][kernel]
    run_as_root("%(manager)s %(cmd)s" % locals())


def upgrade(kernel=False):
    """
    Upgrade all packages, including obsoletes.

    Exclude *kernel* upgrades by default.
    """
    manager = MANAGER
    cmds = {
        'yum -y --color=never': {
            False: '--exclude=kernel* upgrade',
            True: 'upgrade'
        }
    }
    cmd = cmds[manager][kernel]
    run_as_root("%(manager)s %(cmd)s" % locals())


def groupupdate(group, options=None):
    """
    Update an existing software group, skip obsoletes if ``obsoletes=1``
    in ``yum.conf``.

    Extra *options* may be passed to ``yum`` if necessary.
    """
    manager = MANAGER
    if options is None:
        options = []
    elif isinstance(options, str):
        options = [options]
    options = " ".join(options)
    run_as_root('%(manager)s %(options)s groupupdate "%(group)s"' % locals())


def is_installed(pkg_name):
    """
    Check if an RPM package is installed.
    """
    manager = MANAGER
    with settings(
            hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = run("rpm --query %(pkg_name)s" % locals())
        if res.succeeded:
            return True
        return False


def install(packages, repos=None, yes=None, options=None):
    """
    Install one or more RPM packages.

    Extra *repos* may be passed to ``yum`` to enable extra repositories at install time.

    Extra *yes* may be passed to ``yum`` to validate license if necessary.

    Extra *options* may be passed to ``yum`` if necessary
    (e.g. ``['--nogpgcheck', '--exclude=package']``).

    ::

        import fabtools

        # Install a single package, in an alternative install root
        fabtools.rpm.install('emacs', options='--installroot=/my/new/location')

        # Install multiple packages silently
        fabtools.rpm.install([
            'unzip',
            'nano'
        ], '--quiet')

    """
    manager = MANAGER
    if options is None:
        options = []
    elif isinstance(options, str):
        options = [options]
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    if repos:
        for repo in repos:
            options.append('--enablerepo=%(repo)s' % locals())
    options = " ".join(options)
    if isinstance(yes, str):
        run_as_root('yes %(yes)s | %(manager)s %(options)s install %(packages)s' % locals())
    else:
        run_as_root('%(manager)s %(options)s install %(packages)s' % locals())


def groupinstall(group, options=None):
    """
    Install a group of packages.

    You can use ``yum grouplist`` to get the list of groups.

    Extra *options* may be passed to ``yum`` if necessary like
    (e.g. ``['--nogpgcheck', '--exclude=package']``).

    ::

        import fabtools

        # Install development packages
        fabtools.rpm.groupinstall('Development tools')

    """
    manager = MANAGER
    if options is None:
        options = []
    elif isinstance(options, str):
        options = [options]
    options = " ".join(options)
    run_as_root(
        '%(manager)s %(options)s groupinstall "%(group)s"' % locals(),
        pty=False)


def uninstall(packages, options=None):
    """
    Remove one or more packages.

    Extra *options* may be passed to ``yum`` if necessary.

    """
    manager = MANAGER
    if options is None:
        options = []
    elif isinstance(options, str):
        options = [options]
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options = " ".join(options)
    run_as_root('%(manager)s %(options)s remove %(packages)s' % locals())


def groupuninstall(group, options=None):
    """
    Remove an existing software group.

    Extra *options* may be passed to ``yum`` if necessary.

    """
    manager = MANAGER
    if options is None:
        options = []
    elif isinstance(options, str):
        options = [options]
    options = " ".join(options)
    run_as_root('%(manager)s %(options)s groupremove "%(group)s"' % locals())


def repolist(status='', media=None):
    """
    Get the list of ``yum`` repositories.

    Returns enabled repositories by default. Extra *status* may be passed
    to list disabled repositories if necessary.

    Media and debug repositories are kept disabled, except if you pass *media*.

    ::

        import fabtools

        # Install a package that may be included in disabled repositories
        fabtools.rpm.install('vim', fabtools.rpm.repolist('disabled'))

    """
    manager = MANAGER
    with settings(hide('running', 'stdout')):
        if media:
            repos = run_as_root("%(manager)s repolist %(status)s | sed '$d' | sed -n '/repo id/,$p'" % locals())
        else:
            repos = run_as_root("%(manager)s repolist %(status)s | sed '/Media\\|Debug/d' | sed '$d' | sed -n '/repo id/,$p'" % locals())
        return map(lambda line: line.split(' ')[0], repos.splitlines()[1:])
