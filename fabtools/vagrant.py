"""
Vagrant helpers
===============
"""
from __future__ import with_statement

import re

from fabric.api import env, hide, local, settings, task


def version():
    """
    Get the Vagrant version.
    """
    with settings(hide('running')):
        output = local('vagrant --version', capture=True)
    line = output.splitlines()[-1]
    version = re.match(r'Vagrant (?:v(?:ersion )?)?(.*)', line).group(1)
    return tuple(_to_int(part) for part in version.split('.'))


def _to_int(val):
    try:
        return int(val)
    except ValueError:
        return val


def ssh_config(name=''):
    """
    Get the SSH parameters for connecting to a vagrant VM.
    """
    with settings(hide('running')):
        output = local('vagrant ssh-config %s' % name, capture=True)

    config = {}
    for line in output.splitlines()[1:]:
        key, value = line.strip().split(' ', 2)
        config[key] = value
    return config


def _settings_dict(config):
    settings = {}

    user = config['User']
    hostname = config['HostName']
    port = config['Port']

    # Build host string
    host_string = "%s@%s:%s" % (user, hostname, port)

    settings['user'] = user
    settings['hosts'] = [host_string]
    settings['host_string'] = host_string

    # Strip leading and trailing double quotes introduced by vagrant 1.1
    settings['key_filename'] = config['IdentityFile'].strip('"')

    settings['forward_agent'] = (config.get('ForwardAgent', 'no') == 'yes')
    settings['disable_known_hosts'] = True

    return settings


@task
def vagrant(name=''):
    """
    Run the following tasks on a vagrant box.

    First, you need to import this task in your ``fabfile.py``::

        from fabric.api import *
        from fabtools.vagrant import vagrant

        @task
        def some_task():
            run('echo hello')

    Then you can easily run tasks on your current Vagrant box::

        $ fab vagrant some_task

    """
    config = ssh_config(name)

    extra_args = _settings_dict(config)
    env.update(extra_args)


def vagrant_settings(name='', *args, **kwargs):
    """
    Context manager that sets a vagrant VM
    as the remote host.

    Use this context manager inside a task to run commands
    on your current Vagrant box::

        from fabtools.vagrant import vagrant_settings

        with vagrant_settings():
            run('hostname')
    """
    config = ssh_config(name)

    extra_args = _settings_dict(config)
    kwargs.update(extra_args)

    return settings(*args, **kwargs)
