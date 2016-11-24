"""
Users
=====
"""

from pipes import quote
import posixpath
import random
import string

from fabric.api import hide, run, settings, sudo, local

from fabtools.group import (
    exists as _group_exists,
    create as _group_create,
)
from fabtools.files import uncommented_lines
from fabtools.utils import run_as_root


def exists(name):
    """
    Check if a user exists.
    """
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        return run('getent passwd %(name)s' % locals()).succeeded


_SALT_CHARS = string.ascii_letters + string.digits + './'


def _crypt_password(password):
    from crypt import crypt
    random.seed()
    salt = ''
    for _ in range(2):
        salt += random.choice(_SALT_CHARS)
    crypted_password = crypt(password, salt)
    return crypted_password


def create(name, comment=None, home=None, create_home=None, skeleton_dir=None,
           group=None, create_group=True, extra_groups=None, password=None,
           system=False, shell=None, uid=None, ssh_public_keys=None,
           non_unique=False):
    """
    Create a new user and its home directory.

    If *create_home* is ``None`` (the default), a home directory will be
    created for normal users, but not for system users.
    You can override the default behaviour by setting *create_home* to
    ``True`` or ``False``.

    If *system* is ``True``, the user will be a system account. Its UID
    will be chosen in a specific range, and it will not have a home
    directory, unless you explicitely set *create_home* to ``True``.

    If *shell* is ``None``, the user's login shell will be the system's
    default login shell (usually ``/bin/sh``).

    *ssh_public_keys* can be a (local) filename or a list of (local)
    filenames of public keys that should be added to the user's SSH
    authorized keys (see :py:func:`fabtools.user.add_ssh_public_keys`).

    Example::

        import fabtools

        if not fabtools.user.exists('alice'):
            fabtools.user.create('alice')

        with cd('/home/alice'):
            # ...

    """

    # Note that we use useradd (and not adduser), as it is the most
    # portable command to create users across various distributions:
    # http://refspecs.linuxbase.org/LSB_4.1.0/LSB-Core-generic/LSB-Core-generic/useradd.html

    args = []
    if comment:
        args.append('-c %s' % quote(comment))
    if home:
        args.append('-d %s' % quote(home))
    if group:
        args.append('-g %s' % quote(group))
        if create_group:
            if not _group_exists(group):
                _group_create(group)
    if extra_groups:
        groups = ','.join(quote(group) for group in extra_groups)
        args.append('-G %s' % groups)

    if create_home is None:
        create_home = not system
    if create_home is True:
        args.append('-m')
    elif create_home is False:
        args.append('-M')

    if skeleton_dir:
        args.append('-k %s' % quote(skeleton_dir))
    if password:
        crypted_password = _crypt_password(password)
        args.append('-p %s' % quote(crypted_password))
    if system:
        args.append('-r')
    if shell:
        args.append('-s %s' % quote(shell))
    if uid:
        args.append('-u %s' % uid)
        if non_unique:
            args.append('-o')
    args.append(name)
    args = ' '.join(args)
    run_as_root('useradd %s' % args)

    if ssh_public_keys:
        if isinstance(ssh_public_keys, basestring):
            ssh_public_keys = [ssh_public_keys]
        add_ssh_public_keys(name, ssh_public_keys)


def modify(name, comment=None, home=None, move_current_home=False, group=None,
           extra_groups=None, login_name=None, password=None, shell=None,
           uid=None, ssh_public_keys=None, non_unique=False):
    """
    Modify an existing user.

    *ssh_public_keys* can be a (local) filename or a list of (local)
    filenames of public keys that should be added to the user's SSH
    authorized keys (see :py:func:`fabtools.user.add_ssh_public_keys`).

    Example::

        import fabtools

        if fabtools.user.exists('alice'):
            fabtools.user.modify('alice', shell='/bin/sh')

    """

    args = []
    if comment:
        args.append('-c %s' % quote(comment))
    if home:
        args.append('-d %s' % quote(home))
        if move_current_home:
            args.append('-m')
    if group:
        args.append('-g %s' % quote(group))
    if extra_groups:
        groups = ','.join(quote(group) for group in extra_groups)
        args.append('-G %s' % groups)
    if login_name:
        args.append('-l %s' % quote(login_name))
    if password:
        crypted_password = _crypt_password(password)
        args.append('-p %s' % quote(crypted_password))
    if shell:
        args.append('-s %s' % quote(shell))
    if uid:
        args.append('-u %s' % quote(uid))
        if non_unique:
            args.append('-o')

    if args:
        args.append(name)
        args = ' '.join(args)
        run_as_root('usermod %s' % args)

    if ssh_public_keys:
        if isinstance(ssh_public_keys, basestring):
            ssh_public_keys = [ssh_public_keys]
        add_ssh_public_keys(name, ssh_public_keys)


def home_directory(name):
    """
    Get the absolute path to the user's home directory

    Example::

        import fabtools

        home = fabtools.user.home_directory('alice')

    """
    with settings(hide('running', 'stdout')):
        return run('echo ~' + name)


def local_home_directory(name=''):
    """
    Get the absolute path to the local user's home directory

    Example::

        import fabtools

        local_home = fabtools.user.local_home_directory()

    """
    with settings(hide('running', 'stdout')):
        return local('echo ~' + name, capture=True)


def authorized_keys(name):
    """
    Get the list of authorized SSH public keys for the user
    """

    ssh_dir = posixpath.join(home_directory(name), '.ssh')
    authorized_keys_filename = posixpath.join(ssh_dir, 'authorized_keys')

    return uncommented_lines(authorized_keys_filename, use_sudo=True)


def add_ssh_public_key(name, filename):
    """
    Add a public key to the user's authorized SSH keys.

    *filename* must be the local filename of a public key that should be
    added to the user's SSH authorized keys.

    Example::

        import fabtools

        fabtools.user.add_ssh_public_key('alice', '~/.ssh/id_rsa.pub')

    """

    add_ssh_public_keys(name, [filename])


def add_ssh_public_keys(name, filenames):
    """
    Add multiple public keys to the user's authorized SSH keys.

    *filenames* must be a list of local filenames of public keys that
    should be added to the user's SSH authorized keys.

    Example::

        import fabtools

        fabtools.user.add_ssh_public_keys('alice', [
            '~/.ssh/id1_rsa.pub',
            '~/.ssh/id2_rsa.pub',
        ])

    """

    from fabtools.require.files import (
        directory as _require_directory,
        file as _require_file,
    )

    ssh_dir = posixpath.join(home_directory(name), '.ssh')
    _require_directory(ssh_dir, mode='700', owner=name, use_sudo=True)

    authorized_keys_filename = posixpath.join(ssh_dir, 'authorized_keys')
    _require_file(authorized_keys_filename, mode='600', owner=name,
                  use_sudo=True)

    for filename in filenames:

        with open(filename) as public_key_file:
            public_key = public_key_file.read().strip()

        # we don't use fabric.contrib.files.append() as it's buggy
        if public_key not in authorized_keys(name):
            sudo('echo %s >>%s' % (quote(public_key),
                                   quote(authorized_keys_filename)))


def add_host_keys(name, hostname):
    """
    Add all public keys of a host to the user's SSH known hosts file
    """

    from fabtools.require.files import (
        directory as _require_directory,
        file as _require_file,
    )

    ssh_dir = posixpath.join(home_directory(name), '.ssh')
    _require_directory(ssh_dir, mode='700', owner=name, use_sudo=True)

    known_hosts_filename = posixpath.join(ssh_dir, 'known_hosts')
    _require_file(known_hosts_filename, mode='644', owner=name, use_sudo=True)

    known_hosts = uncommented_lines(known_hosts_filename, use_sudo=True)

    with hide('running', 'stdout'):
        res = run('ssh-keyscan -t rsa,dsa %s 2>/dev/null' % hostname)
    for host_key in res.splitlines():
        if host_key not in known_hosts:
            sudo('echo %s >>%s' % (quote(host_key),
                                   quote(known_hosts_filename)))
