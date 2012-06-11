"""
Fabric tools for managing OpenVZ containers

The remote host needs a patched kernel with OpenVZ support
"""
from __future__ import with_statement

from contextlib import contextmanager

from fabric.api import *


def create(ctid, ostemplate=None, config=None, private=None,
           root=None, ipadd=None, hostname=None, **kwargs):
    """
    Create OpenVZ container
    """
    return _vzctl('create', ctid, ostemplate=ostemplate, config=config,
        private=private, root=root, ipadd=ipadd, hostname=hostname, **kwargs)


def destroy(ctid):
    """
    Destroy OpenVZ container
    """
    return _vzctl('destroy', ctid)


def set(ctid, save=True, **kwargs):
    """
    Set OpenVZ container parameters
    """
    return _vzctl('set', ctid, **kwargs)


def start(ctid, wait=False, force=False, **kwargs):
    """
    Start OpenVZ container

    Warning: wait=True is broken with vzctl 3.0.24 on Debian 6.0 (squeeze)
    """
    return _vzctl('start', ctid, wait=wait, force=force, **kwargs)


def stop(ctid, fast=False, **kwargs):
    """
    Stop OpenVZ container
    """
    return _vzctl('stop', ctid, fast=fast, **kwargs)


def restart(ctid, wait=True, force=False, fast=False, **kwargs):
    """
    Restart OpenVZ container
    """
    return _vzctl('restart', ctid, wait=wait, force=force, fast=fast, **kwargs)


def status(ctid):
    """
    Show status of OpenVZ container
    """
    return _vzctl('status', ctid)


def exec2(ctid, command):
    """
    Run command inside OpenVZ container
    """
    return sudo('vzctl exec2 %s %s' % (ctid, command))


def _vzctl(command, ctid, **kwargs):
    args = _expand_args(**kwargs)
    return sudo('vzctl %s %s %s' % (command, ctid, args))


def _expand_args(**kwargs):
    args = []
    for k, v in kwargs.items():
        if isinstance(v, bool):
            if v is True:
                args.append('--%s' % k)
        elif isinstance(v, (list, tuple)):
            for elem in v:
                args.append('--%s %s' % (k, elem))
        elif v is not None:
            args.append('--%s %s' % (k, v))
    return ' '.join(args)


def download_template(name=None, url=None):
    """
    Download an OpenVZ template
    """
    if url is None:
        url = 'http://download.openvz.org/template/precreated/%s.tar.gz' % name

    with cd('/var/lib/vz/template/cache'):
        sudo('wget --progress=dot "%s"' % url)
