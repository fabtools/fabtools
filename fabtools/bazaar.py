#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bzr
===

This module provides low-level tools for managing `Bazaar`_ repositories.  You
should normally not use them directly but rather use the high-level wrapper
:func:`fabtools.require.bazaar.working_copy` instead.

.. _Bazaar: http://bazaar.canonical.com/en/

"""

from __future__ import with_statement

from fabric.api import local
from fabric.api import run
from fabric.api import sudo
from fabric.context_managers import cd

from fabtools.utils import run_as_root


def _run(cmd, use_sudo=False, user=None):
    if use_sudo and user is None:
        run_as_root(cmd)
    elif use_sudo:
        sudo(cmd, user=user)
    else:
        run(cmd)

def checkout(path, use_sudo=False, user=None):
    """
    Reconstitute a working tree for the branch at ``path``.

    :param path: Path of the branch directory.  Must exist.
    :type path: str
    """

    with cd(path):
        _run('bzr checkout --quiet', use_sudo=use_sudo, user=user)

def clone(remote_url, path=None, version=None, force=False,
          use_sudo=False, user=None):
    """
    Clone a remote Bazaar repository into a new directory.

    :param remote_url: URL of the remote repository to clone.
    :type remote_url: str

    :param path: Path of the working copy directory.  Must not exist yet.
    :type path: str

    :param version: revision to fetch from the remote repository
    :type version: str

    :param force: if ``True`` create the new branch even if the target
                  directory already exists but is not a branch or working tree
    :type force: bool

    :param use_sudo: If ``True`` execute ``bzr`` with
                     :func:`fabric.operations.sudo`, else with
                     :func:`fabric.operations.run`.
    :type use_sudo: bool

    :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                 with the given user.  If ``use_sudo is False`` this parameter
                 has no effect.
    :type user: str
    """

    cmd = ['bzr', 'branch', '--quiet']
    if version:
        cmd.extend(['-r', version])
    if force:
        cmd.append('--use-existing-dir')
    cmd.append(remote_url)
    if path is not None:
        cmd.append(path)
    cmd = ' '.join(cmd)

    _run(cmd, use_sudo=use_sudo, user=user)

def get_version(path):
    """
    Return the version of the bzr branch.

    :param path: Path of the working copy directory.  Must exist.
    :type path: str
    """

    cmd = 'bzr revno %s' % path
    revno = run(cmd).strip()
    return revno

def has_local_mods(path):
    """
    Return true if checkout at path has local modifications.

    :param path: Path of the working copy directory.  Must exist.
    :type path: str
    """

    cmd = 'bzr status -S --versioned'
    with cd(path):
        lines = run(cmd).splitlines()

    return len(lines) > 0

def reset(path, use_sudo=False, user=None):
    """
    Reset working tree to the current revision of the branch.
    Discards any changes to tracked files in the working tree since that
    commit.

    :param path: Path of the working copy directory.  Must exist.
    :type path: str

    :param use_sudo: If ``True`` execute ``bzr`` with
                     :func:`fabric.operations.sudo`, else with
                     :func:`fabric.operations.run`.
    :type use_sudo: bool

    :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                 with the given user.  If ``use_sudo is False`` this parameter
                 has no effect.
    :type user: str
    """

    with cd(path):
        _run('bzr revert --quiet', use_sudo=use_sudo, user=user)

def switch_version(path, version=None, use_sudo=False, user=None):
    """
    Switch working tree to specified revno/revid (or latest if not specified).

    :param path: Path of the working copy directory.  Must exist.
    :type path: str

    :param version: revision to switch to
    :type version: str

    :param use_sudo: If ``True`` execute ``bzr`` with
                     :func:`fabric.operations.sudo`, else with
                     :func:`fabric.operations.run`.
    :type use_sudo: bool

    :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                 with the given user.  If ``use_sudo is False`` this parameter
                 has no effect.
    :type user: str
    """

    cmd = ['bzr', 'update']
    if version:
        cmd.extend(['-r', version])
    cmd.append(path)
    cmd = ' '.join(cmd)

    _run(cmd, use_sudo=use_sudo, user=user)

def pull(path, location=None, version=None, force=False,
         use_sudo=False, user=None):
    """
    Pull changes from the default remote repository and update the branch.

    :param path: Path of the working copy directory.  Must exist.
    :type path: str

    :param location: Location to pull from (a branch or merge directive).  If
                     not specified, try to use the default location (parent).
    :type location: str

    :param version: revision to pull from the repository
    :type version: str

    :param force: if ``True`` ignore differences and overwrite overwrite the
                  branch unconditionally
    :type force: bool

    :param use_sudo: If ``True`` execute ``bzr`` with
                     :func:`fabric.operations.sudo`, else with
                     :func:`fabric.operations.run`.
    :type use_sudo: bool

    :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                 with the given user.  If ``use_sudo is False`` this parameter
                 has no effect.
    :type user: str
    """

    cmd = ['bzr', 'pull', '--quiet', '-d', path]
    if version:
        cmd.extend(['-r', version])
    if force:
        cmd.append('--overwrite')
    if location:
        cmd.append(location)
    cmd = ' '.join(cmd)

    _run(cmd, use_sudo=use_sudo, user=user)

def push(location, source=None, version=None, force=False):
    """
    Push changes from the branch at ``source`` to a remote location.

    This requires Bazaar client to be installed on the local host.

    :param location: URL of the target branch / working tree
    :type location: str

    :param source: Location of the branch to push from.  Use current directory
                   if not specified.
    :type source: str

    :param version: revision to push from the repository
    :type version: str

    :param force: if ``True`` ignore differences and overwrite overwrite the
                  branch unconditionally, also create leading directories and
                  push even if remote directory already exists but is not a
                  branch or working tree
    :type force: bool
    """

    cmd = ['bzr', 'push']
    if source:
        cmd.extend(['-d', source])
    if version:
        cmd.extend(['-r', version])
    if force:
        cmd.extend(['--create-prefix', '--use-existing-dir', '--overwrite'])
    cmd.append(location)
    cmd = ' '.join(cmd)

    local(cmd)
