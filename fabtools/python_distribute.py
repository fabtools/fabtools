"""
Python packages
===============

This module provides tools for installing Python packages using
the ``easy_install`` command provided by `distribute`_.

.. _distribute: http://packages.python.org/distribute/

"""
from __future__ import with_statement

from fabric.api import cd, run

from fabtools.utils import run_as_root


def is_distribute_installed():
    """
    Check if `distribute`_ is installed.

    .. _distribute: http://packages.python.org/distribute/
    """
    cmd = '''python -c "import pkg_resources;\
                        print pkg_resources.get_distribution('distribute')"
          '''
    res = run(cmd, quiet=True)
    return res.succeeded and (res.find('distribute') >= 0)


def install_distribute():
    """
    Install the latest version of `distribute`_.

    .. _distribute: http://packages.python.org/distribute/

    ::

        from fabtools.python_distribute import *

        if not is_distribute_installed():
            install_distribute()

    """
    with cd("/tmp"):
        run("curl --silent -O http://python-distribute.org/distribute_setup.py")
        run_as_root("python distribute_setup.py")


def install(packages, upgrade=False, use_sudo=False):
    """
    Install Python packages with ``easy_install``.

    Examples::

        import fabtools

        # Install a single package
        fabtools.python_distribute.install('package', use_sudo=True)

        # Install a list of packages
        fabtools.python_distribute.install(['pkg1', 'pkg2'], use_sudo=True)

    .. note:: most of the time, you'll want to use
              :py:func:`fabtools.python.install()` instead,
              which uses ``pip`` to install packages.

    """
    func = use_sudo and run_as_root or run
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options = []
    if upgrade:
        options.append("-U")
    options = " ".join(options)
    func('easy_install %(options)s %(packages)s' % locals())
