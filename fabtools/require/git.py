"""
Git
===

This module provides high-level tools for managing `Git`_ repositories.

.. _Git: http://git-scm.com/

"""

from __future__ import with_statement

from fabtools import git
from fabtools.files import is_dir


def working_copy(remote_url, path=None, branch="master", update=True,
                 use_sudo=False, user=None):
    """
    Require a working copy of the repository from the ``remote_url``.

    Clones or pulls from the repository under ``remote_url`` and checks out
    ``branch``.

    :param remote_url: URL of the remote repository (e.g.
                       https://github.com/ronnix/fabtools.git).  The given URL
                       will be the ``origin`` remote of the working copy.
    :type remote_url: str

    :param path: Absolute or relative path of the working copy on the
                 filesystem.  If this directory doesn't exist yet, a new
                 working copy is created through ``git clone``.  If the
                 directory does exist *and* ``update == True``, a
                 ``git pull`` is issued.  If ``path is None`` the ``git clone``
                 is issued in the current working directory and the directory
                 name of the working copy is created by ``git``.
    :type path: str

    :param branch: Branch to switch to after cloning or pulling.
    :type branch: str

    :param update: Whether or not to update an existing working copy via
                   ``git pull``.
    :type update: bool

    :param use_sudo: If ``True`` execute ``git`` with
                     :func:`fabric.operations.sudo`, else with
                     :func:`fabric.operations.run`.
    :type use_sudo: bool

    :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                 with the given user.  If ``use_sudo is False`` this parameter
                 has no effect.
    :type user: str
    """

    if is_dir(path, use_sudo=use_sudo) and update:
        # git pull
        git.pull(path=path, use_sudo=use_sudo, user=user)

    elif is_dir(path, use_sudo=use_sudo) and not update:
        # do nothing
        return

    elif not is_dir(path, use_sudo=use_sudo):
        # git clone
        git.clone(remote_url, path=path, use_sudo=use_sudo, user=user)
        if path is None:
            path = remote_url.split('/')[-1].replace('.git', '')

    else:
        raise ValueError("Invalid combination of parameters.")

    git.checkout(path=path, branch=branch, use_sudo=use_sudo, user=user)
