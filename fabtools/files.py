"""
Fabric tools for managing files and directories
"""
import os.path
from fabric.api import *
from fabric.contrib.files import upload_template as _upload_template


def is_file(path, use_sudo=False):
    """
    Check if a path exists, and is a file
    """
    func = use_sudo and sudo or run
    with settings(hide('running', 'warnings'), warn_only=True):
        return func('[ -f "%(path)s" ]' % locals()).succeeded


def is_dir(path, use_sudo=False):
    """
    Check if a path exists, and is a directory
    """
    func = use_sudo and sudo or run
    with settings(hide('running', 'warnings'), warn_only=True):
        return func('[ -d "%(path)s" ]' % locals()).succeeded


def is_link(path, use_sudo=False):
    """
    Check if a path exists, and is a symbolic link
    """
    func = use_sudo and sudo or run
    with settings(hide('running', 'warnings'), warn_only=True):
        return func('[ -L "%(path)s" ]' % locals()).succeeded


def upload_template(filename, template, context=None, use_sudo=False,
                  user="root", mkdir=False, chown=False):
    """
    Upload a template file
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
    Compute MD5 sum
    """
    func = use_sudo and sudo or run
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = func('md5sum %(filename)s' % locals())
    if res.failed:
        warn(res)
        return None
    return res.split()[0]
