"""
Supervisor processes
====================

This module provides high-level tools for managing long-running
processes using `supervisor`_.

.. _supervisor: http://supervisord.org/

"""

from fabtools.files import watch
from fabtools.supervisor import update_config, process_status, start_process
from fabtools.system import UnsupportedFamily, distrib_family


def process(name, use_pip=False, **kwargs):
    """
    Require a supervisor process to be running. Installs supervisor
    from the default system package manager unless ``use_pip`` is
    truthy.

    Keyword arguments will be used to build the program configuration
    file. Some useful arguments are:

    - ``command``: complete command including arguments (**required**)
    - ``directory``: absolute path to the working directory
    - ``user``: run the process as this user
    - ``stdout_logfile``: absolute path to the log file

    You should refer to the `supervisor documentation`_ for the
    complete list of allowed arguments.

    .. note:: the default values for the following arguments differs from
              the ``supervisor`` defaults:

              - ``autorestart``: defaults to ``true``
              - ``redirect_stderr``: defaults to ``true``

    Example::

        from fabtools import require

        require.supervisor.process('myapp',
            command='/path/to/venv/bin/myapp --config production.ini --someflag',
            directory='/path/to/working/dir',
            user='alice',
            stdout_logfile='/path/to/logs/myapp.log',
            )

    .. _supervisor documentation: http://supervisord.org/configuration.html#program-x-section-values

    """

    from fabtools.require import file as require_file
    from fabtools.require.python import package as require_python_package
    from fabtools.require.deb import package as require_deb_package
    from fabtools.require.rpm import package as require_rpm_package
    from fabtools.require.arch import package as require_arch_package
    from fabtools.require.service import started as require_started

    # configure installation. override default package installation w/ use_pip
    family = distrib_family()
    if family == 'debian':
        require_package = require_deb_package
        package_name = 'supervisor'
        daemon_name = 'supervisor'
        filename = '/etc/supervisor/conf.d/%(name)s.conf' % locals()
    elif family == 'redhat':
        require_package = require_rpm_package
        package_name = 'supervisord'
        daemon_name = 'supervisord'
        filename = '/etc/supervisord.d/%(name)s.ini' % locals()
    elif family == 'arch':
        require_package = require_arch_package
        package_name = 'supervisor'
        daemon_name = 'supervisord'
        filename = '/etc/supervisor.d/%(name)s.ini' % locals()
    else:
        raise UnsupportedFamily(supported=['debian', 'redhat', 'arch'])
    if use_pip:
        require_package = require_python_package
        package_name = 'supervisor'

    # install supervisor and make sure its started
    require_package(package_name)
    require_started(daemon_name)

    # Set default parameters
    params = {}
    params.update(kwargs)
    params.setdefault('autorestart', 'true')
    params.setdefault('redirect_stderr', 'true')

    # Build config file from parameters
    lines = []
    lines.append('[program:%(name)s]' % locals())
    for key, value in sorted(params.items()):
        lines.append("%s=%s" % (key, value))

    # Upload config file
    with watch(filename, callback=update_config, use_sudo=True):
        require_file(filename, contents='\n'.join(lines), use_sudo=True)

    # Start the process if needed
    if process_status(name) == 'STOPPED':
        start_process(name)
