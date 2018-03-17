"""
Bazaar
======

This module provides high-level tools for managing `Bazaar`_ repositories.

.. _Bazaar: http://bazaar.canonical.com/en/

"""

from __future__ import with_statement

import os
import posixpath

from six.moves.urllib.parse import urlparse

from fabric.api import abort, env, puts, run
from fabric.colors import cyan

from fabtools import bazaar, utils
from fabtools.files import is_dir
from fabtools.system import UnsupportedFamily


def command():
    """
    Require the ``bzr`` command-line tool.

    Example::

        from fabric.api import run
        from fabtools import require

        require.bazaar.command()
        run('bzr --help')

    """
    from fabtools.require.deb import package as require_deb_package
    from fabtools.require.rpm import package as require_rpm_package
    from fabtools.require.portage import package as require_portage_package
    from fabtools.system import distrib_family

    res = run('bzr --version', quiet=True)
    if res.failed:
        family = distrib_family()
        if family == 'debian':
            require_deb_package('bzr')
        elif family == 'gentoo':
            require_portage_package('bzr')
        elif family == 'redhat':
            require_rpm_package('bzr')
        else:
            raise UnsupportedFamily(supported=['debian', 'redhat', 'gentoo'])


def working_copy(source, target=None, version=None, update=True, force=False,
                 use_sudo=False, user=None):
    """
    Require a working copy of the repository from ``source``.

    If ``source`` is a URL to a remote branch, that branch will be
    cloned/pulled on the remote host.

    If ``source`` refers to a local branch, that branch will be pushed from
    local host to the remote.  This requires Bazaar client to be installed on
    the local host.

    The ``target`` is optional, and defaults to the last segment of the
    source repository URL.

    If the ``target`` does not exist, this will clone the specified source
    branch into ``target`` path.

    If the ``target`` exists and ``update`` is ``True``, it will transfer
    changes from the source branch, then update the working copy.

    If the ``target`` exists and ``update`` is ``False``, nothing will be done.

    :param source: URL/path of the source branch
    :type source: str

    :param target: Absolute or relative path of the working copy on the
                   filesystem.  If this directory doesn't exist yet, a new
                   working copy is created.  If the directory does exist *and*
                   ``update == True`` it will be updated.  If
                   ``target is None`` last segment of ``source`` is used.
    :type target: str

    :param version: Revision to check out / switch to
    :type version: str

    :param update: Whether or not to pull and update remote changesets.
    :type update: bool

    :param force: If ``True`` ignore differences and overwrite the ``target``
                  branch unconditionally, also create leading directories and
                  the target branch even if remote directory already exists
                  but is not a branch or working tree
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

    command()

    suargs = dict(use_sudo=use_sudo, user=user)
    vfsargs = dict(version=version, force=force, **suargs)  # vers, force, su
    before = None
    exists = False
    local_mods = False
    src_url = urlparse(source)

    def ensure_tree(dir):
        if not is_dir(posixpath.join(dir, '.bzr', 'checkout'),
                      use_sudo=use_sudo):
            bazaar.checkout(dir, **suargs)

    if target is None:
        src_path = os.getcwd() if src_url.path == '.' else src_url.path
        target = src_path.split('/')[-1]

    if is_dir(target, use_sudo=use_sudo) and not update:
        puts(("Working tree '%s' already exists, "
              "not updating (update=False)") % target)
        return

    if is_dir(posixpath.join(target, '.bzr'), use_sudo=use_sudo):
        ensure_tree(target)

        before = bazaar.get_version(target)
        exists = True
        local_mods = bazaar.has_local_mods(target)

        if local_mods and force:
            bazaar.reset(target, **suargs)
        elif local_mods:
            abort(("Working tree '%s' has local modifications; "
                   "use force=True to discard them") % target)

    if src_url.scheme in ('', 'file'):  # local source
        target_url = 'bzr+ssh://%s/%s' % (
            env.host_string, utils.abspath(target))
        bazaar.push(target_url, source=source, version=version, force=force)
        ensure_tree(target)
        bazaar.switch_version(target, version=version, **suargs)
    else:  # remote source
        if exists:
            bazaar.pull(target, location=source, **vfsargs)
            bazaar.switch_version(target, version=version, **suargs)
        else:
            bazaar.clone(source, target, **vfsargs)
    after = bazaar.get_version(target)

    if before != after or local_mods:
        chg = 'created at revision'
        if before:
            mods = ' (with local modifications)' if local_mods else ''
            chg = 'changed from revision %s%s to' % (before, mods)
        puts(cyan('Working tree %r %s %s' % (target, chg, after)))
    else:
        puts(cyan('Working tree %r unchanged (no updates)' % target))
