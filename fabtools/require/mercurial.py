"""
Mercurial
=========

This module provides high-level tools for managing `Mercurial`_ repositories.

.. _Mercurial: http://mercurial.selenic.com/

"""

from fabric.api import run

from fabtools import mercurial
from fabtools.files import is_dir
from fabtools.system import UnsupportedFamily, distrib_family


def command():
    """
    Require the ``hg`` command-line tool.

    Example::

        from fabric.api import run
        from fabtools import require

        require.mercurial.command()
        run('hg --help')

    """
    from fabtools.require.deb import package as require_deb_package
    from fabtools.require.rpm import package as require_rpm_package
    from fabtools.require.portage import package as require_portage_package

    res = run('hg --version', quiet=True)
    if res.failed:
        family = distrib_family()
        if family == 'debian':
            require_deb_package('mercurial')
        elif family == 'gentoo':
            require_portage_package('mercurial')
        elif family == 'redhat':
            require_rpm_package('mercurial')
        else:
            raise UnsupportedFamily(supported=['debian', 'redhat', 'gentoo'])


def working_copy(remote_url, path=None, branch="default", update=True,
                 use_sudo=False, user=None):
    """
    Require a working copy of the repository from the ``remote_url``.

    The ``path`` is optional, and defaults to the last segment of the
    remote repository URL.

    If the ``path`` does not exist, this will clone the remote
    repository and check out the specified branch.

    If the ``path`` exists and ``update`` is ``True``, it will pull
    changes from the remote repository, check out the specified branch,
    then update the working copy.

    If the ``path`` exists and ``update`` is ``False``, it will only
    check out the specified branch, without pulling remote changesets.

    :param remote_url: URL of the remote repository
    :type remote_url: str

    :param path: Absolute or relative path of the working copy on the
                 filesystem.  If this directory doesn't exist yet, a new
                 working copy is created through ``hg clone``.  If the
                 directory does exist *and* ``update == True``, a
                 ``hg pull && hg up`` is issued.  If ``path is None`` the
                 ``hg clone`` is issued in the current working directory and
                 the directory name of the working copy is created by ``hg``.
    :type path: str

    :param branch: Branch or tag to check out.  If the given value is a tag
                   name, update must be ``False`` or consecutive calls will
                   fail.
    :type branch: str

    :param update: Whether or not to pull and update remote changesets.
    :type update: bool

    :param use_sudo: If ``True`` execute ``hg`` with
                     :func:`fabric.operations.sudo`, else with
                     :func:`fabric.operations.run`.
    :type use_sudo: bool

    :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                 with the given user.  If ``use_sudo is False`` this parameter
                 has no effect.
    :type user: str
    """

    command()

    if path is None:
        path = remote_url.split('/')[-1]

    if is_dir(path, use_sudo=use_sudo):
        mercurial.pull(path, use_sudo=use_sudo, user=user)
        if update:
            mercurial.update(path=path, branch=branch, use_sudo=use_sudo,
                             user=user)
    elif not is_dir(path, use_sudo=use_sudo):
        mercurial.clone(remote_url, path=path, use_sudo=use_sudo, user=user)
        mercurial.update(
            path=path, branch=branch, use_sudo=use_sudo, user=user)
    else:
        raise ValueError("Invalid combination of parameters.")
