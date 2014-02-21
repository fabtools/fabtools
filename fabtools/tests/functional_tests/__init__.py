from pipes import quote
import logging
import os

from nose.plugins.skip import SkipTest

from fabric.api import env, hide, lcd, local, settings
from fabric.state import connections

from fabtools.vagrant import version


MIN_VAGRANT_VERSION = (1, 3)


HERE = os.path.dirname(__file__)


def setup_package():
    _check_vagrant_version()

    vagrant_box = os.environ.get('FABTOOLS_TEST_BOX')
    if vagrant_box is None:
        raise SkipTest("Functional tests (set FABTOOLS_TEST_BOX to choose a Vagrant base box)")

    vagrant_provider = os.environ.get('FABTOOLS_TEST_PROVIDER')

    _configure_logging()
    _stop_vagrant_machine()
    _init_vagrant_machine(vagrant_box)
    _start_vagrant_machine(vagrant_provider)
    _target_vagrant_machine()
    _set_optional_http_proxy()
    _update_package_index()


def _check_vagrant_version():
    vagrant_version = version()
    if vagrant_version is None:
        raise SkipTest("Functional tests: Vagrant is required")
    elif vagrant_version < MIN_VAGRANT_VERSION:
        min_version = ".".join(map(str, MIN_VAGRANT_VERSION))
        found_version = ".".join(map(str, vagrant_version))
        raise SkipTest("Functional tests: Vagrant >= %s is required (%s found)" % (min_version, found_version))


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


