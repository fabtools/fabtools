"""
Idempotent API for managing files and directories
"""
import os.path
from urlparse import urlparse

from fabric.api import *
from fabtools.files import is_file, is_dir, md5sum


def directory(path, use_sudo=False, owner='', group='', mode=''):
    """
    I can haz directory
    """
    func = use_sudo and sudo or run
    if not is_dir(path):
        func('mkdir -p "%(path)s"' % locals())
        if owner:
            func('chown %(owner)s:%(group)s "%(path)s"' % locals())
        if mode:
            func('chmod %(mode)s "%(path)s"' % locals())


def downloaded_file(url, filename=None, md5=None, use_sudo=False):
    """
    I can haz downloaded file
    """
    func = use_sudo and sudo or run

    if not filename:
        filename = os.path.basename(urlparse(url).path)

    download = True
    if is_file(filename):
        if (md5 is None) or (md5 == md5sum(filename)):
            download = False

    if download:
        func('wget --progress=dots %(url)s' % locals())
