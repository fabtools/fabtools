"""
Users
=====
"""
from __future__ import with_statement

from crypt import crypt
from pipes import quote
import random
import string

from fabric.api import *


def exists(name):
    """
    Check if a user exists.
    """
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        return run('getent passwd %(name)s' % locals()).succeeded


_SALT_CHARS = string.ascii_letters + string.digits + './'


def _crypt_password(password):
    random.seed()
    salt = ''
    for _ in range(2):
        salt += random.choice(_SALT_CHARS)
    crypted_password = crypt(password, salt)
    return crypted_password


def create(name, comment=None, home=None, group=None, extra_groups=None,
    create_home=True, skeleton_dir=None, password=None, system=False,
    shell=None, uid=None):
    """
    Create a new user and its home directory.

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
    if extra_groups:
        groups = ','.join(quote(group) for group in groups)
        args.append('-G %s' % groups)
    if create_home:
        args.append('-m')
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
        args.append('-u %s' % quote(uid))
    args.append(name)
    args = ' '.join(args)
    sudo('useradd %s' % args)


def modify(name, comment=None, home=None, move_current_home=False, group=None,
    extra_groups=None, login_name=None, password=None, shell=None, uid=None):
    """
    Modify an existing user.

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
        groups = ','.join(quote(group) for group in groups)
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
    args.append(name)
    args = ' '.join(args)
    sudo('usermod %s' % args)
