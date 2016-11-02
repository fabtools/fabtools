"""
Files and directories
=====================
"""

from pipes import quote
import os

from fabric.api import (
    abort,
    env,
    hide,
    run,
    settings,
    sudo,
    warn,
)
from fabric.contrib.files import upload_template as _upload_template
from fabric.contrib.files import exists

from fabtools.utils import run_as_root


def is_file(path, use_sudo=False):
    """
    Check if a path exists, and is a file.
    """
    func = use_sudo and run_as_root or run
    with settings(hide('running', 'warnings'), warn_only=True):
        return func('[ -f "%(path)s" ]' % locals()).succeeded


def is_dir(path, use_sudo=False):
    """
    Check if a path exists, and is a directory.
    """
    func = use_sudo and run_as_root or run
    with settings(hide('running', 'warnings'), warn_only=True):
        return func('[ -d "%(path)s" ]' % locals()).succeeded


def is_link(path, use_sudo=False):
    """
    Check if a path exists, and is a symbolic link.
    """
    func = use_sudo and run_as_root or run
    with settings(hide('running', 'warnings'), warn_only=True):
        return func('[ -L "%(path)s" ]' % locals()).succeeded


def owner(path, use_sudo=False):
    """
    Get the owner name of a file or directory.
    """
    func = use_sudo and run_as_root or run
    # I'd prefer to use quiet=True, but that's not supported with older
    # versions of Fabric.
    with settings(hide('running', 'stdout'), warn_only=True):
        result = func('stat -c %%U "%(path)s"' % locals())
        if result.failed and 'stat: illegal option' in result:
            # Try the BSD version of stat
            return func('stat -f %%Su "%(path)s"' % locals())
        else:
            return result


def group(path, use_sudo=False):
    """
    Get the group name of a file or directory.
    """
    func = use_sudo and run_as_root or run
    # I'd prefer to use quiet=True, but that's not supported with older
    # versions of Fabric.
    with settings(hide('running', 'stdout'), warn_only=True):
        result = func('stat -c %%G "%(path)s"' % locals())
        if result.failed and 'stat: illegal option' in result:
            # Try the BSD version of stat
            return func('stat -f %%Sg "%(path)s"' % locals())
        else:
            return result


def mode(path, use_sudo=False):
    """
    Get the mode (permissions) of a file or directory.

    Returns a string such as ``'0755'``, representing permissions as
    an octal number.
    """
    func = use_sudo and run_as_root or run
    # I'd prefer to use quiet=True, but that's not supported with older
    # versions of Fabric.
    with settings(hide('running', 'stdout'), warn_only=True):
        result = func('stat -c %%a "%(path)s"' % locals())
        if result.failed and 'stat: illegal option' in result:
            # Try the BSD version of stat
            return func('stat -f %%Op "%(path)s"|cut -c 4-6' % locals())
        else:
            return result


def umask(use_sudo=False):
    """
    Get the user's umask.

    Returns a string such as ``'0002'``, representing the user's umask
    as an octal number.

    If `use_sudo` is `True`, this function returns root's umask.
    """
    func = use_sudo and run_as_root or run
    return func('umask')


def upload_template(filename, destination, context=None, use_jinja=False,
                    template_dir=None, use_sudo=False, backup=True,
                    mirror_local_mode=False, mode=None,
                    mkdir=False, chown=False, user=None):
    """
    Upload a template file.

    This is a wrapper around :func:`fabric.contrib.files.upload_template`
    that adds some extra parameters.

    If ``mkdir`` is True, then the remote directory will be created, as
    the current user or as ``user`` if specified.

    If ``chown`` is True, then it will ensure that the current user (or
    ``user`` if specified) is the owner of the remote file.
    """

    if mkdir:
        remote_dir = os.path.dirname(destination)
        if use_sudo:
            sudo('mkdir -p %s' % quote(remote_dir), user=user)
        else:
            run('mkdir -p %s' % quote(remote_dir))

    _upload_template(
        filename=filename,
        destination=destination,
        context=context,
        use_jinja=use_jinja,
        template_dir=template_dir,
        use_sudo=use_sudo,
        backup=backup,
        mirror_local_mode=mirror_local_mode,
        mode=mode,
    )

    if chown:
        if user is None:
            user = env.user
        run_as_root('chown %s: %s' % (user, quote(destination)))


def md5sum(filename, use_sudo=False):
    """
    Compute the MD5 sum of a file.
    """
    func = use_sudo and run_as_root or run
    with settings(hide('running', 'stdout', 'stderr', 'warnings'),
                  warn_only=True):
        # Linux (LSB)
        if exists(u'/usr/bin/md5sum'):
            res = func(u'/usr/bin/md5sum %(filename)s' % locals())
        # BSD / OS X
        elif exists(u'/sbin/md5'):
            res = func(u'/sbin/md5 -r %(filename)s' % locals())
        # SmartOS Joyent build
        elif exists(u'/opt/local/gnu/bin/md5sum'):
            res = func(u'/opt/local/gnu/bin/md5sum %(filename)s' % locals())
        # SmartOS Joyent build
        # (the former doesn't exist, at least on joyent_20130222T000747Z)
        elif exists(u'/opt/local/bin/md5sum'):
            res = func(u'/opt/local/bin/md5sum %(filename)s' % locals())
        # Try to find ``md5sum`` or ``md5`` on ``$PATH`` or abort
        else:
            md5sum = func(u'which md5sum')
            md5 = func(u'which md5')
            if exists(md5sum):
                res = func('%(md5sum)s %(filename)s' % locals())
            elif exists(md5):
                res = func('%(md5)s %(filename)s' % locals())
            else:
                abort('No MD5 utility was found on this system.')

    if res.succeeded:
        parts = res.split()
        _md5sum = len(parts) > 0 and parts[0] or None
    else:
        warn(res)
        _md5sum = None

    return _md5sum


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
        from fabtools.service import restart

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
        from fabtools.service import restart

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


def uncommented_lines(filename, use_sudo=False):
    """
    Get the lines of a remote file, ignoring empty or commented ones
    """
    func = run_as_root if use_sudo else run
    res = func('cat %s' % quote(filename), quiet=True)
    if res.succeeded:
        return [line for line in res.splitlines()
                if line and not line.startswith('#')]
    else:
        return []


def getmtime(path, use_sudo=False):
    """
    Return the time of last modification of path.
    The return value is a number giving the number of seconds since the epoch

    Same as :py:func:`os.path.getmtime()`
    """
    func = use_sudo and run_as_root or run
    with settings(hide('running', 'stdout')):
        return int(func('stat -c %%Y "%(path)s" ' % locals()).strip())


def copy(source, destination, recursive=False, use_sudo=False):
    """
    Copy a file or directory
    """
    func = use_sudo and run_as_root or run
    options = '-r ' if recursive else ''
    func('/bin/cp {0}{1} {2}'.format(
        options, quote(source), quote(destination)))


def move(source, destination, use_sudo=False):
    """
    Move a file or directory
    """
    func = use_sudo and run_as_root or run
    func('/bin/mv {0} {1}'.format(quote(source), quote(destination)))


def symlink(source, destination, use_sudo=False):
    """
    Create a symbolic link to a file or directory
    """
    func = use_sudo and run_as_root or run
    func('/bin/ln -s {0} {1}'.format(quote(source), quote(destination)))


def remove(path, recursive=False, use_sudo=False):
    """
    Remove a file or directory
    """
    func = use_sudo and run_as_root or run
    options = '-r ' if recursive else ''
    func('/bin/rm {0}{1}'.format(options, quote(path)))
