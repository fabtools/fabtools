"""
Redis
=====

This module provides high-level tools for managing `Redis`_ instances.

.. _Redis: http://redis.io/

"""
from __future__ import with_statement

from fabtools.files import is_file, watch
from fabtools.deb import *


VERSION = '2.4.17'

BINARIES = [
    'redis-benchmark',
    'redis-check-aof',
    'redis-check-dump',
    'redis-cli',
    'redis-server',
]


def installed_from_source(version=VERSION):
    """
    Require Redis to be installed from source.

    The compiled binaries will be installed in ``/opt/redis-{version}/``.
    """
    from fabtools import require

    require.user('redis')

    dest_dir = '/opt/redis-%(version)s' % locals()
    require.directory(dest_dir, use_sudo=True, owner='redis')

    if not is_file('%(dest_dir)s/redis-server' % locals()):

        with cd('/tmp'):

            # Download and unpack the tarball
            tarball = 'redis-%(version)s.tar.gz' % locals()
            require.file(tarball, url='http://redis.googlecode.com/files/' + tarball)
            run('tar xzf %(tarball)s' % locals())

            # Compile and install binaries
            require.deb.package('build-essential')
            with cd('redis-%(version)s' % locals()):
                run('make')

                for filename in BINARIES:
                    sudo('cp -pf src/%(filename)s %(dest_dir)s/' % locals())
                    sudo('chown redis: %(dest_dir)s/%(filename)s' % locals())


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
    from fabtools import require

    installed_from_source(version)

    require.directory('/etc/redis', use_sudo=True, owner='redis')
    require.directory('/var/db/redis', use_sudo=True, owner='redis')
    require.directory('/var/log/redis', use_sudo=True, owner='redis')
    require.directory('/var/run/redis', use_sudo=True, owner='redis')

    # Required for background saving
    with settings(warn_only=True):
        require.system.sysctl('vm.overcommit_memory', '1')

    # Set default parameters
    params = {}
    params.update(kwargs)
    params.setdefault('bind', '127.0.0.1')
    params.setdefault('port', '6379')
    params.setdefault('logfile', '/var/log/redis/redis-%(name)s.log' % locals())
    params.setdefault('loglevel', 'verbose')
    params.setdefault('dbfilename', '/var/db/redis/redis-%(name)s-dump.rdb' % locals())
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
        require.file(config_filename, contents='\n'.join(lines),
            use_sudo=True, owner='redis')

    # Use supervisord to manage process
    process_name = 'redis_%s' % name
    require.supervisor.process(process_name,
        user='redis',
        directory='/var/run/redis',
        command="%(redis_server)s %(config_filename)s" % locals())

    # Restart if needed
    if config.changed:
        fabtools.supervisor.restart_process(process_name)
