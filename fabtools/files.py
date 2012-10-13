"""
Files and directories
=====================
"""
from __future__ import with_statement

import os.path

from fabric.api import *
from fabric.contrib.files import upload_template as _upload_template


def is_file(path, use_sudo=False):
    """
    Check if a path exists, and is a file.
    """
    func = use_sudo and sudo or run
    with settings(hide('running', 'warnings'), warn_only=True):
        return func('[ -f "%(path)s" ]' % locals()).succeeded


def is_dir(path, use_sudo=False):
    """
    Check if a path exists, and is a directory.
    """
    func = use_sudo and sudo or run
    with settings(hide('running', 'warnings'), warn_only=True):
        return func('[ -d "%(path)s" ]' % locals()).succeeded


def is_link(path, use_sudo=False):
    """
    Check if a path exists, and is a symbolic link.
    """
    func = use_sudo and sudo or run
    with settings(hide('running', 'warnings'), warn_only=True):
        return func('[ -L "%(path)s" ]' % locals()).succeeded


def owner(path, use_sudo=False):
    """
    Get the owner name of a file or directory.
    """
    func = use_sudo and sudo or run
    with settings(hide('running', 'stdout')):
        return func('stat -c %%U "%(path)s"' % locals())


def group(path, use_sudo=False):
    """
    Get the group name of a file or directory.
    """
    func = use_sudo and sudo or run
    with settings(hide('running', 'stdout')):
        return func('stat -c %%G "%(path)s"' % locals())


def mode(path, use_sudo=False):
    """
    Get the mode (permissions) of a file or directory.

    Returns a string such as ``'0755'``, representing permissions as
    an octal number.
    """
    func = use_sudo and sudo or run
    with settings(hide('running', 'stdout')):
        return func('stat -c %%a "%(path)s"' % locals())


def upload_template(filename, template, context=None, use_sudo=False,
                  user="root", mkdir=False, chown=False):
    """
    Upload a template file.
    """
    if mkdir:
        d = os.path.dirname(filename)
        if use_sudo:
            sudo('mkdir -p "%s"' % d, user=user)
        else:
            run('mkdir -p "%s"' % d)
    _upload_template(os.path.join("templates", template), filename,
                    context=context, use_sudo=use_sudo)
    if chown:
        sudo('chown %s:%s "%s"' % (user, user, filename))


def md5sum(filename, use_sudo=False):
    """
    Compute the MD5 sum of a file.
    """
    func = use_sudo and sudo or run
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = func('md5sum %(filename)s' % locals())
    if res.failed:
        warn(res)
        return None
    return res.split()[0]


class watch(object):
    """
    Context manager to watch for changes to the contents of some files.

    The *filenames* argument can be either a string (single filename)
    or a list (multiple filenames).

    You can read the *changed* attribute at the end of the block to
    check if the contents of any of the watched files has changed.

    You can also provide a *callback* that will be called at the end of
    the block if the contents of any of the watched files has changed.

    Example using an explicit check::

        from fabric.contrib.files import comment, uncomment

        from fabtools.files import watch
        from fabtools.services import restart

        # Edit configuration file
        with watch('/etc/daemon.conf') as config:
            uncomment('/etc/daemon.conf', 'someoption')
            comment('/etc/daemon.conf', 'otheroption')

        # Restart daemon if needed
        if config.changed:
            restart('daemon')

    Same example using a callback::

        from functools import partial

        from fabric.contrib.files import comment, uncomment

        from fabtools.files import watch
        from fabtools.services import restart

        with watch('/etc/daemon.conf', callback=partial(restart, 'daemon')):
            uncomment('/etc/daemon.conf', 'someoption')
            comment('/etc/daemon.conf', 'otheroption')

    """

    def __init__(self, filenames, callback=None, use_sudo=False):
        if isinstance(filenames, basestring):
            self.filenames = [filenames]
        else:
            self.filenames = filenames
        self.callback = callback
        self.use_sudo = use_sudo
        self.digest = dict()
        self.changed = False

    def __enter__(self):
        with settings(hide('warnings')):
            for filename in self.filenames:
                self.digest[filename] = md5sum(filename, self.use_sudo)
        return self

    def __exit__(self, type, value, tb):
        for filename in self.filenames:
            if md5sum(filename, self.use_sudo) != self.digest[filename]:
                self.changed = True
                break
        if self.changed and self.callback:
            self.callback()
