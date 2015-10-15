"""
Debian packages
===============

This module provides tools to manage Debian/Ubuntu packages
and repositories.

"""

from fabric.api import hide, run, settings

from fabtools.utils import run_as_root
from fabtools.files import getmtime, is_file


MANAGER = 'DEBIAN_FRONTEND=noninteractive apt-get'


def update_index(quiet=True):
    """
    Update APT package definitions.
    """
    options = "--quiet --quiet" if quiet else ""
    run_as_root("%s %s update" % (MANAGER, options))


def upgrade(safe=True):
    """
    Upgrade all packages.
    """
    manager = MANAGER
    if safe:
        cmd = 'upgrade'
    else:
        cmd = 'dist-upgrade'
    run_as_root("%(manager)s --assume-yes %(cmd)s" % locals(), pty=False)


def is_installed(pkg_name):
    """
    Check if a package is installed.
    """
    with settings(
            hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = run("dpkg -s %(pkg_name)s" % locals())
        for line in res.splitlines():
            if line.startswith("Status: "):
                status = line[8:]
                if "installed" in status.split(' '):
                    return True
        return False


def install(packages, update=False, options=None, version=None):
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

        # Install a specific version
        fabtools.deb.install('emacs', version='23.3+1-1ubuntu9')

    """
    manager = MANAGER
    if update:
        update_index()
    if options is None:
        options = []
    if version is None:
        version = ''
    if version and not isinstance(packages, list):
        version = '=' + version
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options.append("--quiet")
    options.append("--assume-yes")
    options = " ".join(options)
    cmd = '%(manager)s install %(options)s %(packages)s%(version)s' % locals()
    run_as_root(cmd, pty=False)


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
    cmd = '%(manager)s %(command)s %(options)s %(packages)s' % locals()
    run_as_root(cmd, pty=False)


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
        run_as_root('echo "%(pkg_name)s %(q_name)s %(q_type)s %(q_answer)s" | debconf-set-selections' % locals())


def get_selections():
    """
    Get the state of ``dkpg`` selections.

    Returns a dict with state => [packages].
    """
    with settings(hide('stdout')):
        res = run_as_root('dpkg --get-selections')
    selections = dict()
    for line in res.splitlines():
        package, status = line.split()
        selections.setdefault(status, list()).append(package)
    return selections


def apt_key_exists(keyid):
    """
    Check if the given key id exists in apt keyring.
    """

    # Command extracted from apt-key source
    gpg_cmd = 'gpg --ignore-time-conflict --no-options --no-default-keyring --keyring /etc/apt/trusted.gpg'

    with settings(hide('everything'), warn_only=True):
        res = run('%(gpg_cmd)s --fingerprint %(keyid)s' % locals())

    return res.succeeded


def _check_pgp_key(path, keyid):
    with settings(hide('everything')):
        return not run('gpg --with-colons %(path)s | cut -d: -f 5 | grep -q \'%(keyid)s$\'' % locals())


def add_apt_key(filename=None, url=None, keyid=None, keyserver='subkeys.pgp.net', update=False):
    """
    Trust packages signed with this public key.

    Example::

        import fabtools

        # Varnish signing key from URL and verify fingerprint)
        fabtools.deb.add_apt_key(keyid='C4DEFFEB', url='http://repo.varnish-cache.org/debian/GPG-key.txt')

        # Nginx signing key from default key server (subkeys.pgp.net)
        fabtools.deb.add_apt_key(keyid='7BD9BF62')

        # From custom key server
        fabtools.deb.add_apt_key(keyid='7BD9BF62', keyserver='keyserver.ubuntu.com')

        # From a file
        fabtools.deb.add_apt_key(keyid='7BD9BF62', filename='nginx.asc'
    """

    if keyid is None:
        if filename is not None:
            run_as_root('apt-key add %(filename)s' % locals())
        elif url is not None:
            run_as_root('wget %(url)s -O - | apt-key add -' % locals())
        else:
            raise ValueError(
                'Either filename, url or keyid must be provided as argument')
    else:
        if filename is not None:
            _check_pgp_key(filename, keyid)
            run_as_root('apt-key add %(filename)s' % locals())
        elif url is not None:
            tmp_key = '/tmp/tmp.fabtools.key.%(keyid)s.key' % locals()
            run_as_root('wget %(url)s -O %(tmp_key)s' % locals())
            _check_pgp_key(tmp_key, keyid)
            run_as_root('apt-key add %(tmp_key)s' % locals())
        else:
            keyserver_opt = '--keyserver %(keyserver)s' % locals() if keyserver is not None else ''
            run_as_root('apt-key adv %(keyserver_opt)s --recv-keys %(keyid)s' % locals())

    if update:
        update_index()


def last_update_time():
    """
    Get the time of last APT index update

    This is the last modification time of ``/var/lib/apt/periodic/fabtools-update-success-stamp``.

    Returns ``-1`` if there was no update before.

    Example::

        import fabtools

        print(fabtools.deb.last_update_time())
        # 1377603808.02

    """
    STAMP = '/var/lib/apt/periodic/fabtools-update-success-stamp'
    if not is_file(STAMP):
        return -1
    return getmtime(STAMP)
