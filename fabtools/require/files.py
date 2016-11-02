"""
Files and directories
=====================

This module provides high-level tools for managing files and
directories.

"""

from pipes import quote
from tempfile import mkstemp
from urlparse import urlparse
import hashlib
import os

from fabric.api import hide, put, run, settings

from fabtools.files import (
    group as _group,
    is_file,
    is_dir,
    md5sum,
    mode as _mode,
    owner as _owner,
    umask,
)
from fabtools.utils import run_as_root


BLOCKSIZE = 2 ** 20  # 1MB


def directory(path, use_sudo=False, owner='', group='', mode=''):
    """
    Require a directory to exist.

    ::

        from fabtools import require

        require.directory('/tmp/mydir', owner='alice', use_sudo=True)

    .. note:: This function can be accessed directly from the
              ``fabtools.require`` module for convenience.

    """
    func = use_sudo and run_as_root or run

    if not is_dir(path):
        func('mkdir -p "%(path)s"' % locals())

    # Ensure correct owner
    if (owner and _owner(path, use_sudo) != owner) or \
       (group and _group(path, use_sudo) != group):
        func('chown %(owner)s:%(group)s "%(path)s"' % locals())

    # Ensure correct mode
    if mode and _mode(path, use_sudo) != mode:
        func('chmod %(mode)s "%(path)s"' % locals())


def directories(path_list, use_sudo=False, owner='', group='', mode=''):
    """
    Require a list of directories to exist.

    ::

        from fabtools import require
        dirs=[
            '/tmp/mydir',
            '/tmp/mydear',
            '/tmp/my/dir'
        ]
        require.directories(dirs, owner='alice', mode='750')

    .. note:: This function can be accessed directly from the
              ``fabtools.require`` module for convenience.
    """
    for path in path_list:
        directory(path, use_sudo, owner, group, mode)


def file(path=None, contents=None, source=None, url=None, md5=None,
         use_sudo=False, owner=None, group='', mode=None, verify_remote=True,
         temp_dir='/tmp'):
    """
    Require a file to exist and have specific contents and properties.

    You can provide either:

    - *contents*: the required contents of the file::

        from fabtools import require

        require.file('/tmp/hello.txt', contents='Hello, world')

    - *source*: the local path of a file to upload::

        from fabtools import require

        require.file('/tmp/hello.txt', source='files/hello.txt')

    - *url*: the URL of a file to download (*path* is then optional)::

        from fabric.api import cd
        from fabtools import require

        with cd('tmp'):
            require.file(url='http://example.com/files/hello.txt')

    If *verify_remote* is ``True`` (the default), then an MD5 comparison
    will be used to check whether the remote file is the same as the
    source. If this is ``False``, the file will be assumed to be the
    same if it is present. This is useful for very large files, where
    generating an MD5 sum may take a while.

    When providing either the *contents* or the *source* parameter, Fabric's
    ``put`` function will be used to upload the file to the remote host.
    When ``use_sudo`` is ``True``, the file will first be uploaded to a temporary
    directory, then moved to its final location. The default temporary
    directory is ``/tmp``, but can be overridden with the *temp_dir* parameter.
    If *temp_dir* is an empty string, then the user's home directory will
    be used.

    If `use_sudo` is `True`, then the remote file will be owned by root,
    and its mode will reflect root's default *umask*. The optional *owner*,
    *group* and *mode* parameters can be used to override these properties.

    .. note:: This function can be accessed directly from the
              ``fabtools.require`` module for convenience.

    """
    func = use_sudo and run_as_root or run

    # 1) Only a path is given
    if path and not (contents or source or url):
        assert path
        if not is_file(path):
            func('touch "%(path)s"' % locals())

    # 2) A URL is specified (path is optional)
    elif url:
        if not path:
            path = os.path.basename(urlparse(url).path)

        if not is_file(path) or md5 and md5sum(path) != md5:
            func('wget --progress=dot:mega %(url)s -O %(path)s' % locals())

    # 3) A local filename, or a content string, is specified
    else:
        if source:
            assert not contents
            t = None
        else:
            fd, source = mkstemp()
            t = os.fdopen(fd, 'w')
            t.write(contents)
            t.close()

        if verify_remote:
            # Avoid reading the whole file into memory at once
            digest = hashlib.md5()
            f = open(source, 'rb')
            try:
                while True:
                    d = f.read(BLOCKSIZE)
                    if not d:
                        break
                    digest.update(d)
            finally:
                f.close()
        else:
            digest = None

        if (not is_file(path, use_sudo=use_sudo) or
                (verify_remote and
                    md5sum(path, use_sudo=use_sudo) != digest.hexdigest())):
            with settings(hide('running')):
                put(source, path, use_sudo=use_sudo, temp_dir=temp_dir)

        if t is not None:
            os.unlink(source)

    # Ensure correct owner
    if use_sudo and owner is None:
        owner = 'root'
    if (owner and _owner(path, use_sudo) != owner) or \
       (group and _group(path, use_sudo) != group):
        func('chown %(owner)s:%(group)s "%(path)s"' % locals())

    # Ensure correct mode
    if use_sudo and mode is None:
        mode = oct(0666 & ~int(umask(use_sudo=True), base=8))
    if mode and _mode(path, use_sudo) != mode:
        func('chmod %(mode)s "%(path)s"' % locals())


def template_file(path=None, template_contents=None, template_source=None,
                  context=None, **kwargs):
    """
    Require a file whose contents is defined by a template.
    """
    if template_contents is None:
        with open(template_source) as template_file:
            template_contents = template_file.read()

    if context is None:
        context = {}

    file(path=path, contents=template_contents % context, **kwargs)


def temporary_directory(template=None):
    """
    Require a temporary directory.

    The directory is created using the ``mktemp`` command. It will
    be created in ``/tmp``, unless the ``TMPDIR`` environment variable
    is set to another location. ::

        from fabtools.require.files import temporary_directory

        tmp_dir = temporary_directory()

    You can choose a specific location and name template for the
    temporary directory: ::

        from fabtools.require.files import temporary_directory

        tmp_dir = temporary_directory('/var/tmp/temp.XXXXXX')

    You can also call this function as a context manager. In this case,
    the directory and its contents will be automatically deleted when
    exiting the block: ::

        from pipes import quote
        from posixpath import join

        from fabtools.require.files import temporary_directory

        with temporary_directory() as tmp_dir:
            path = join(tmp_dir, 'foo')
            run('touch %s' % quote(path))

    """
    options = ['--directory']
    if template:
        options.append(template)
    options = ' '.join(options)
    with hide('running', 'stdout'):
        path = run('mktemp %s' % options)
    return TemporaryDirectory(path)


class TemporaryDirectory(str):

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        run('rm -rf %s' % quote(self))
