"""
Mercurial
=========

This module provides low-level tools for managing `Mercurial`_ repositories.
You should normally not use them directly but rather use the high-level wrapper
:func:`fabtools.require.mercurial.working_copy` instead.

.. _Mercurial: http://mercurial.selenic.com/

"""

from fabric.api import run
from fabric.api import sudo
from fabric.context_managers import cd

from fabtools.utils import run_as_root


def clone(remote_url, path=None, use_sudo=False, user=None):
    """
    Clone a remote Mercurial repository into a new directory.

    :param remote_url: URL of the remote repository to clone.
    :type remote_url: str

    :param path: Path of the working copy directory.  Must not exist yet.
    :type path: str

    :param use_sudo: If ``True`` execute ``hg`` with
                     :func:`fabric.operations.sudo`, else with
                     :func:`fabric.operations.run`.
    :type use_sudo: bool

    :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                 with the given user.  If ``use_sudo is False`` this parameter
                 has no effect.
    :type user: str
    """

    cmd = 'hg --quiet clone %s' % remote_url
    if path is not None:
        cmd = cmd + ' %s' % path

    if use_sudo and user is None:
        run_as_root(cmd)
    elif use_sudo:
        sudo(cmd, user=user)
    else:
        run(cmd)


def update(path, branch="default", use_sudo=False, user=None, force=False):
    """
    Merge changes to a working copy and/or switch branches.

    :param path: Path of the working copy directory.  This directory must exist
                 and be a Mercurial working copy.
    :type path: str

    :param use_sudo: If ``True`` execute ``hg`` with
                     :func:`fabric.operations.sudo`, else with
                     :func:`fabric.operations.run`.
    :type use_sudo: bool

    :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                 with the given user.  If ``use_sudo is False`` this parameter
                 has no effect.
    :type user: str

    """
    cmd = "hg up %s" % branch

    with cd(path):
        if use_sudo and user is None:
            run_as_root(cmd)
        elif use_sudo:
            sudo(cmd, user=user)
        else:
            run(cmd)


def pull(path, use_sudo=False, user=None):
    """
    Pull changes from the default remote repository.

    :param path: Path of the working copy directory.  This directory must exist
                 and be a Mercurial working copy with a default remote to pull
                 from.
    :type path: str

    :param use_sudo: If ``True`` execute ``hg`` with
                     :func:`fabric.operations.sudo`, else with
                     :func:`fabric.operations.run`.
    :type use_sudo: bool

    :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                 with the given user.  If ``use_sudo is False`` this parameter
                 has no effect.
    :type user: str
    """

    if not path:
        raise ValueError("Path to the working copy is needed to pull from a "
                         "remote repository.")

    cmd = 'hg pull'

    with cd(path):
        if use_sudo and user is None:
            run_as_root(cmd)
        elif use_sudo:
            sudo(cmd, user=user)
        else:
            run(cmd)
