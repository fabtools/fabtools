"""
Python packages
===============

This module provides tools for installing Python packages using
the ``easy_install`` command provided by `setuptools`_.

.. _setuptools: http://pythonhosted.org/setuptools/

"""

from fabric.api import cd, run

from fabtools.utils import download, run_as_root


EZ_SETUP_URL = 'https://bootstrap.pypa.io/ez_setup.py'


def package_version(name, python_cmd='python'):
    """
    Get the installed version of a package

    Returns ``None`` if it can't be found.
    """
    cmd = '''%(python_cmd)s -c \
        "import pkg_resources;\
        dist = pkg_resources.get_distribution('%(name)s');\
        print(dist.version)"
        ''' % locals()
    res = run(cmd, quiet=True)
    if res.succeeded:
        return res
    else:
        return None


def is_setuptools_installed(python_cmd='python'):
    """
    Check if `setuptools`_ is installed.

    .. _setuptools: http://pythonhosted.org/setuptools/
    """
    version = package_version('setuptools', python_cmd=python_cmd)
    return (version is not None)


def install_setuptools(python_cmd='python', use_sudo=True):
    """
    Install the latest version of `setuptools`_.

    ::

        import fabtools

        fabtools.python_setuptools.install_setuptools()

    """

    setuptools_version = package_version('setuptools', python_cmd)
    distribute_version = package_version('distribute', python_cmd)

    if setuptools_version is None:
        _install_from_scratch(python_cmd, use_sudo)
    else:
        if distribute_version is None:
            _upgrade_from_setuptools(python_cmd, use_sudo)
        else:
            _upgrade_from_distribute(python_cmd, use_sudo)


def _install_from_scratch(python_cmd, use_sudo):
    """
    Install setuptools from scratch using installer
    """

    with cd("/tmp"):
        download(EZ_SETUP_URL)

        command = '%(python_cmd)s ez_setup.py' % locals()
        if use_sudo:
            run_as_root(command)
        else:
            run(command)

        run('rm -f ez_setup.py')


def _upgrade_from_setuptools(python_cmd, use_sudo):
    """
    Upgrading from setuptools 0.6 to 0.7+ is supported
    """
    _easy_install(['-U', 'setuptools'], python_cmd, use_sudo)


def _upgrade_from_distribute(python_cmd, use_sudo):
    """
    Upgrading from distribute 0.6 to setuptools 0.7+ directly is not
    supported. We need to upgrade distribute to version 0.7, which is
    a dummy package acting as a wrapper to install setuptools 0.7+.
    """
    _easy_install(['-U', 'distribute'], python_cmd, use_sudo)


def install(packages, upgrade=False, use_sudo=False, python_cmd='python'):
    """
    Install Python packages with ``easy_install``.

    Examples::

        import fabtools

        # Install a single package
        fabtools.python_setuptools.install('package', use_sudo=True)

        # Install a list of packages
        fabtools.python_setuptools.install(['pkg1', 'pkg2'], use_sudo=True)

    .. note:: most of the time, you'll want to use
              :py:func:`fabtools.python.install()` instead,
              which uses ``pip`` to install packages.

    """
    argv = []
    if upgrade:
        argv.append("-U")
    if isinstance(packages, basestring):
        argv.append(packages)
    else:
        argv.extend(packages)
    _easy_install(argv, python_cmd, use_sudo)


def _easy_install(argv, python_cmd, use_sudo):
    """
    Install packages using easy_install

    We don't know if the easy_install command in the path will be the
    right one, so we use the setuptools entry point to call the script's
    main function ourselves.
    """
    command = """python -c "\
        from pkg_resources import load_entry_point;\
        ez = load_entry_point('setuptools', 'console_scripts', 'easy_install');\
        ez(argv=%(argv)r)\
    """ % locals()
    if use_sudo:
        run_as_root(command)
    else:
        run(command)
