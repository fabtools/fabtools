"""
Idempotent API for managing files and directories
"""
from __future__ import with_statement

import hashlib
import os, os.path
from tempfile import mkstemp
from urlparse import urlparse

from fabric.api import *
from fabtools.files import is_file, is_dir, md5sum


BLOCKSIZE = 2 ** 20  # 1MB


def directory(path, use_sudo=False, owner='', group='', mode=''):
    """
    Require a directory
    """
    func = use_sudo and sudo or run
    if not is_dir(path):
        func('mkdir -p "%(path)s"' % locals())
        if owner:
            func('chown %(owner)s:%(group)s "%(path)s"' % locals())
        if mode:
            func('chmod %(mode)s "%(path)s"' % locals())


def file(path=None, contents=None, source=None, url=None, md5=None,
         use_sudo=False, owner=None, group='', mode=None, verify_remote=True):
    """
    Require a file

    You can provide either:
    - contents: the required contents of the file
    - source: the filename of a local file to upload
    - url: the address of a file to download (path is optional)

    If verify_remote is True (the default), then an MD5 comparison will be used
    to check whether the remote file is the same as the source. If this is
    False, the file will be assumed to be the same if it is present. This is
    useful for very large files, where generating an MD5 sum may take a while.
    """
    func = use_sudo and sudo or run

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
            func('wget --progress=dot %(url)s' % locals())

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
                if source:
                    put(source, path, use_sudo=use_sudo)
                else:
                    put(tmp_file.name, path, use_sudo=use_sudo)
                    os.remove(tmp_file.name)

        if t is not None:
            os.unlink(source)

    # Ensure correct owner
    if owner:
        func('chown %(owner)s:%(group)s "%(path)s"' % locals())

    # Ensure correct mode
    if mode:
        func('chmod %(mode)s "%(path)s"' % locals())


def template_file(path=None, template_contents=None, template_source=None, context=None, **kwargs):
    """
    Require a file whose contents is defined by a template
    """
    if template_contents is None:
        with open(template_source) as template_file:
            template_contents = template_file.read()

    if context is None:
        context = {}

    file(path=path, contents=template_contents % context, **kwargs)
