from pipes import quote
import logging
import os

from fabric.api import env, hide, lcd, local, settings
from fabric.state import connections


HERE = os.path.dirname(__file__)


def setup_package():
    base_box = os.environ.get('FABTOOLS_TEST_BOX', 'precise64')
    provider = os.environ.get('FABTOOLS_TEST_PROVIDER')
    _configure_logging()
    _stop_vagrant_machine()
    _init_vagrant_machine(base_box)
    _start_vagrant_machine(provider)
    _target_vagrant_machine()
    _set_optional_http_proxy()
    _update_package_index()


def _configure_logging():
    logger = logging.getLogger('paramiko')
    logger.setLevel(logging.WARN)


def _init_vagrant_machine(base_box):
    with lcd(HERE):
        with settings(hide('stdout')):
            local('rm -f Vagrantfile')
            local('vagrant init %s' % quote(base_box))


def _start_vagrant_machine(provider):
    with lcd(HERE):
        with settings(hide('stdout')):
            if provider:
                local('vagrant up --provider %s' % quote(provider))
            else:
                local('vagrant up')


def _stop_vagrant_machine():
    with lcd(HERE):
        with settings(hide('stdout', 'warnings'), warn_only=True):
            local('vagrant halt')
            local('vagrant destroy -f')


def _target_vagrant_machine():
    config = _vagrant_ssh_config()
    _set_fabric_env(
        host=config['HostName'],
        port=config['Port'],
        user=config['User'],
        key_filename=config['IdentityFile'].strip('"'),
    )
    _clear_fabric_connection_cache()


def _vagrant_ssh_config():
    with lcd(HERE):
        with settings(hide('running')):
            output = local('vagrant ssh-config', capture=True)
    config = {}
    for line in output.splitlines()[1:]:
        key, value = line.strip().split(' ', 2)
        config[key] = value
    return config


def _set_fabric_env(host, port, user, key_filename):
    env.host_string = env.host = "%s:%s" % (host, port)
    env.user = user
    env.key_filename = key_filename
    env.disable_known_hosts = True


def _set_optional_http_proxy():
    http_proxy = os.environ.get('FABTOOLS_HTTP_PROXY')
    if http_proxy is not None:
        env.shell_env['http_proxy'] = http_proxy


def _clear_fabric_connection_cache():
    if env.host_string in connections:
        del connections[env.host_string]


def _update_package_index():
    from fabtools.system import distrib_family
    family = distrib_family()
    if family == 'debian':
        from fabtools.deb import update_index
        update_index()


# def teardown_package(self):
#     _stop_vagrant_machine()


