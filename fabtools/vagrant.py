from fabric.api import *


def ssh_config(name=''):
    """
    Get the SSH parameters for a vagrant VM
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

    settings['host_string'] = "%s@%s:%s" % (user, hostname, port)
    settings['user'] = user
    settings['key_filename'] = config['IdentityFile']
    settings['forward_agent'] = (config.get('ForwardAgent', 'no') == 'yes')
    settings['disable_known_hosts'] = True

    return settings


@task
def vagrant(name=''):
    """
    Run the following tasks on a vagrant box
    """
    config = ssh_config(name)

    extra_args = _settings_dict(config)
    env.update(extra_args)


def vagrant_settings(name='', *args, **kwargs):
    """
    Context manager that sets a vagrant VM
    as the remote host
    """
    config = ssh_config(name)

    extra_args = _settings_dict(config)
    kwargs.update(extra_args)

    return settings(*args, **kwargs)
