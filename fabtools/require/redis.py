"""
Redis
=====

This module provides high-level tools for managing `Redis`_ instances.

.. _Redis: http://redis.io/

"""
from __future__ import with_statement

from fabric.api import cd, run, settings

from fabtools.files import is_file, watch
from fabtools.system import distrib_family
from fabtools.utils import run_as_root
import fabtools.supervisor


VERSION = '2.6.13'

BINARIES = [
    'redis-benchmark',
    'redis-check-aof',
    'redis-check-dump',
    'redis-cli',
    'redis-sentinel',
    'redis-server',
]


def installed_from_source(version=VERSION):
    """
    Require Redis to be installed from source.

    The compiled binaries will be installed in ``/opt/redis-{version}/``.
    """
    from fabtools.require import directory as require_directory
    from fabtools.require import file as require_file
    from fabtools.require import user as require_user
    from fabtools.require.deb import packages as require_deb_packages
    from fabtools.require.rpm import packages as require_rpm_packages

    family = distrib_family()

    if family == 'debian':
        require_deb_packages([
            'build-essential',
        ])

    elif family == 'redhat':
        require_rpm_packages([
            'gcc',
            'make',
        ])

    require_user('redis', home='/var/lib/redis', system=True)
    require_directory('/var/lib/redis', owner='redis', use_sudo=True)

    dest_dir = '/opt/redis-%(version)s' % locals()
    require_directory(dest_dir, use_sudo=True, owner='redis')

    if not is_file('%(dest_dir)s/redis-server' % locals()):

        with cd('/tmp'):

            # Download and unpack the tarball
            tarball = 'redis-%(version)s.tar.gz' % locals()
            url = 'http://redis.googlecode.com/files/' + tarball
            require_file(tarball, url=url)
            run('tar xzf %(tarball)s' % locals())

            # Compile and install binaries
            with cd('redis-%(version)s' % locals()):
                run('make')

                for filename in BINARIES:
                    run_as_root('cp -pf src/%(filename)s %(dest_dir)s/' % locals())
                    run_as_root('chown redis: %(dest_dir)s/%(filename)s' % locals())


def instance(name, version=VERSION, **kwargs):
    """
    Require a Redis instance to be running.

    The instance will be managed using supervisord, as a process named
    ``redis_{name}``, running as the ``redis`` user.

    ::

        from fabtools import require
        from fabtools.supervisor import process_status

        require.redis.installed_from_source()

        require.redis.instance('db1', port='6379')
        require.redis.instance('db2', port='6380')

        print process_status('redis_db1')
        print process_status('redis_db2')

    .. seealso:: :ref:`supervisor_module` and
                 :ref:`require_supervisor_module`


    """
    from fabtools.require import directory as require_directory
    from fabtools.require import file as require_file
    from fabtools.require.supervisor import process as require_process
    from fabtools.require.system import sysctl as require_sysctl

    installed_from_source(version)

    require_directory('/etc/redis', use_sudo=True, owner='redis')
    require_directory('/var/db/redis', use_sudo=True, owner='redis')
    require_directory('/var/log/redis', use_sudo=True, owner='redis')
    require_directory('/var/run/redis', use_sudo=True, owner='redis')

    # Required for background saving
    with settings(warn_only=True):
        require_sysctl('vm.overcommit_memory', '1')

    # Set default parameters
    params = {}
    params.update(kwargs)
    params.setdefault('bind', '127.0.0.1')
    params.setdefault('port', '6379')
    params.setdefault('logfile', '/var/log/redis/redis-%(name)s.log' % locals())
    params.setdefault('loglevel', 'verbose')
    params.setdefault('dir', '/var/db/redis')
    params.setdefault('dbfilename', 'redis-%(name)s-dump.rdb' % locals())
    params.setdefault('save', ['900 1', '300 10', '60 10000'])

    # Build config file from parameters
    # (keys such as 'save' may result in multiple config lines)
    lines = []
    for key, value in sorted(params.items()):
        if isinstance(value, list):
            for elem in value:
                lines.append("%s %s" % (key, elem))
        else:
            lines.append("%s %s" % (key, value))

    redis_server = '/opt/redis-%(version)s/redis-server' % locals()
    config_filename = '/etc/redis/%(name)s.conf' % locals()

    # Upload config file
    with watch(config_filename, use_sudo=True) as config:
        require_file(config_filename, contents='\n'.join(lines),
                     use_sudo=True, owner='redis')

    # Use supervisord to manage process
    process_name = 'redis_%s' % name
    require_process(
        process_name,
        user='redis',
        directory='/var/run/redis',
        command="%(redis_server)s %(config_filename)s" % locals(),
    )

    # Restart if needed
    if config.changed:
        fabtools.supervisor.restart_process(process_name)
