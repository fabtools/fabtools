"""
Redis
=====

This module provides high-level tools for managing `Redis`_ instances.

.. _Redis: http://redis.io/

"""

from fabric.api import cd, run, settings

from fabtools.files import is_file, watch
from fabtools.system import distrib_family
from fabtools.utils import run_as_root
import fabtools.supervisor


VERSION = '2.6.16'

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
            url = _download_url(version) + tarball
            require_file(tarball, url=url)
            run('tar xzf %(tarball)s' % locals())

            # Compile and install binaries
            with cd('redis-%(version)s' % locals()):
                run('make')

                for filename in BINARIES:
                    run_as_root(
                        'cp -pf src/%(filename)s %(dest_dir)s/' % locals())
                    run_as_root(
                        'chown redis: %(dest_dir)s/%(filename)s' % locals())


def _download_url(version):
    if _parse_version(version) <= (2, 6, 14):
        return 'http://redis.googlecode.com/files/'
    else:
        return 'http://download.redis.io/releases/'


def _parse_version(version):
    return tuple(map(int, version.split('.')))


def instance(name, version=VERSION, bind='127.0.0.1', port=6379, **kwargs):
    """
    Require a Redis instance to be running.

    The required Redis version will be automatically installed using
    :py:func:`fabtools.require.redis.installed_from_source` if needed.

    You can specify the IP address and port on which to listen to using the
    *bind* and *port* parameters.

    .. warning::
        Redis is designed to be accessed by trusted clients inside trusted
        environments. It is usually not a good idea to expose the Redis
        instance directly to the internet. Therefore, with the default
        settings, the Redis instance will only listen to local clients.

    If you want to make your Redis instance accessible to other servers
    over an untrusted network, you should probably add some firewall rules
    to restrict access. For example: ::

            from fabtools import require
            from fabtools.shorewall import Ping, SSH, hosts, rule

            # The computers that will need to talk to the Redis server
            REDIS_CLIENTS = [
                'web1.example.com',
                'web2.example.com',
            ]

            # The Redis server port
            REDIS_PORT = 6379

            # Setup a basic firewall
            require.shorewall.firewall(
                rules=[
                    Ping(),
                    SSH(),
                    rule(port=REDIS_PORT, source=hosts(REDIS_CLIENTS)),
                ]
            )

            # Make the Redis instance listen on all interfaces
            require.redis.instance('mydb', bind='0.0.0.0', port=REDIS_PORT)

    .. seealso:: `Redis Security <http://redis.io/topics/security>`_

    You can also use any valid Redis configuration directives as extra
    keyword arguments. For directives that can be repeated on multiple
    lines (such as ``save``), you can supply a list of values.

    The instance will be managed using supervisord, as a process named
    ``redis_{name}``, running as the ``redis`` user.

    ::

        from fabtools import require
        from fabtools.supervisor import process_status

        require.redis.instance('mydb')

        print process_status('redis_mydb')

    .. seealso:: :ref:`supervisor_module` and
                 :ref:`require_supervisor_module`

    The default settings enable persistence using periodic RDB snapshots
    saved in the `/var/db/redis` directory.

    You may want to use AOF persistence instead: ::

        require.redis.instance('mydb', appendonly='yes', save=[])

    In certain situations, you may want to disable persistence completely: ::

        require.redis.instance('cache', port=6380, save=[])

    .. seealso:: `Redis Persistence <http://redis.io/topics/persistence>`_

    """
    from fabtools.require import directory as require_directory
    from fabtools.require import file as require_file
    from fabtools.require.supervisor import process as require_process
    from fabtools.require.system import sysctl as require_sysctl

    installed_from_source(version)

    require_directory('/etc/redis', use_sudo=True, owner='redis')
    require_directory('/var/db/redis', use_sudo=True, owner='redis')
    require_directory('/var/log/redis', use_sudo=True, owner='redis')

    # Required for background saving
    with settings(warn_only=True):
        require_sysctl('vm.overcommit_memory', '1')

    # Set default parameters
    params = {}
    params.update(kwargs)
    params.setdefault('bind', bind)
    params.setdefault('port', port)
    params.setdefault(
        'logfile', '/var/log/redis/redis-%(name)s.log' % locals())
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
        directory='/var/run',
        command="%(redis_server)s %(config_filename)s" % locals(),
    )

    # Restart if needed
    if config.changed:
        fabtools.supervisor.restart_process(process_name)
