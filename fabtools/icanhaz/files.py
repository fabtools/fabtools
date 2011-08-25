"""
Idempotent API for managing files and directories
"""
from fabric.api import *
from fabtools.files import is_dir


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
