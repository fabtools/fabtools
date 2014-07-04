"""
Git
===

This module provides low-level tools for managing `Git`_ repositories.  You
should normally not use them directly but rather use the high-level wrapper
:func:`fabtools.require.git.working_copy` instead.

.. _Git: http://git-scm.com/

"""

from fabric.api import run
from fabric.api import sudo
from fabric.context_managers import cd

from fabtools.utils import run_as_root


def clone(remote_url, path=None, use_sudo=False, user=None):
    """
    Clone a remote Git repository into a new directory.

    :param remote_url: URL of the remote repository to clone.
    :type remote_url: str

    :param path: Path of the working copy directory.  Must not exist yet.
    :type path: str

    :param use_sudo: If ``True`` execute ``git`` with
                     :func:`fabric.operations.sudo`, else with
                     :func:`fabric.operations.run`.
    :type use_sudo: bool

    :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                 with the given user.  If ``use_sudo is False`` this parameter
                 has no effect.
    :type user: str
    """

    cmd = 'git clone --quiet %s' % remote_url
    if path is not None:
        cmd = cmd + ' %s' % path

    if use_sudo and user is None:
        run_as_root(cmd)
    elif use_sudo:
        sudo(cmd, user=user)
    else:
        run(cmd)


def add_remote(path, name, remote_url, use_sudo=False, user=None, fetch=True):
    """
    Add a remote Git repository into a directory.

    :param path: Path of the working copy directory.  This directory must exist
                 and be a Git working copy with a default remote to fetch from.
    :type path: str

    :param use_sudo: If ``True`` execute ``git`` with
                     :func:`fabric.operations.sudo`, else with
                     :func:`fabric.operations.run`.
    :type use_sudo: bool

    :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                 with the given user.  If ``use_sudo is False`` this parameter
                 has no effect.
    :type user: str

    :param name: name for the remote repository
    :type name: str

    :param remote_url: URL of the remote repository
    :type remote_url: str

    :param fetch: If ``True`` execute ``git remote add -f``
    :type fetch: bool
    """
    if path is None:
        raise ValueError("Path to the working copy is needed to add a remote")

    if fetch:
        cmd = 'git remote add -f %s %s' % (name, remote_url)
    else:
        cmd = 'git remote add %s %s' % (name, remote_url)

    with cd(path):
        if use_sudo and user is None:
            run_as_root(cmd)
        elif use_sudo:
            sudo(cmd, user=user)
        else:
            run(cmd)


def fetch(path, use_sudo=False, user=None, remote=None):
    """
    Fetch changes from the default remote repository.

    This will fetch new changesets, but will not update the contents of
    the working tree unless yo do a merge or rebase.

    :param path: Path of the working copy directory.  This directory must exist
                 and be a Git working copy with a default remote to fetch from.
    :type path: str

    :param use_sudo: If ``True`` execute ``git`` with
                     :func:`fabric.operations.sudo`, else with
                     :func:`fabric.operations.run`.
    :type use_sudo: bool

    :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                 with the given user.  If ``use_sudo is False`` this parameter
                 has no effect.
    :type user: str

    :type remote: Fetch this remote or default remote if is None
    :type remote: str
    """

    if path is None:
        raise ValueError("Path to the working copy is needed to fetch from a "
                         "remote repository.")

    if remote is not None:
        cmd = 'git fetch %s' % remote
    else:
        cmd = 'git fetch'

    with cd(path):
        if use_sudo and user is None:
            run_as_root(cmd)
        elif use_sudo:
            sudo(cmd, user=user)
        else:
            run(cmd)


def pull(path, use_sudo=False, user=None, force=False):
    """
    Fetch changes from the default remote repository and merge them.

    :param path: Path of the working copy directory.  This directory must exist
                 and be a Git working copy with a default remote to pull from.
    :type path: str

    :param use_sudo: If ``True`` execute ``git`` with
                     :func:`fabric.operations.sudo`, else with
                     :func:`fabric.operations.run`.
    :type use_sudo: bool

    :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                 with the given user.  If ``use_sudo is False`` this parameter
                 has no effect.
    :type user: str
    :param force: If ``True``, append the ``--force`` option to the command.
    :type force: bool
    """

    if path is None:
        raise ValueError("Path to the working copy is needed to pull from a "
                         "remote repository.")

    options = []
    if force:
        options.append('--force')
    options = ' '.join(options)

    cmd = 'git pull %s' % options

    with cd(path):
        if use_sudo and user is None:
            run_as_root(cmd)
        elif use_sudo:
            sudo(cmd, user=user)
        else:
            run(cmd)


def checkout(path, branch="master", use_sudo=False, user=None, force=False):
    """
    Checkout a branch to the working directory.

    :param path: Path of the working copy directory.  This directory must exist
                 and be a Git working copy.
    :type path: str

    :param branch: Name of the branch to checkout.
    :type branch: str

    :param use_sudo: If ``True`` execute ``git`` with
                     :func:`fabric.operations.sudo`, else with
                     :func:`fabric.operations.run`.
    :type use_sudo: bool

    :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                 with the given user.  If ``use_sudo is False`` this parameter
                 has no effect.
    :type user: str
    :param force: If ``True``, append the ``--force`` option to the command.
    :type force: bool
    """

    if path is None:
        raise ValueError("Path to the working copy is needed to checkout a "
                         "branch")

    options = []
    if force:
        options.append('--force')
    options = ' '.join(options)

    cmd = 'git checkout %s %s' % (branch, options)

    with cd(path):
        if use_sudo and user is None:
            run_as_root(cmd)
        elif use_sudo:
            sudo(cmd, user=user)
        else:
            run(cmd)
