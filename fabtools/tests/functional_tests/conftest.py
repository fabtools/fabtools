from pipes import quote
import logging
import os
import sys

from mock import patch
import pytest

from fabric.api import env, hide, lcd, local, settings
from fabric.state import connections

from fabtools.vagrant import version as _vagrant_version


HERE = os.path.dirname(__file__)


VAGRANT_VERSION = _vagrant_version()
MIN_VAGRANT_VERSION = (1, 3)


@pytest.yield_fixture(scope='session', autouse=True)
def setup_package():
    _check_vagrant_version()
    vagrant_box = os.environ.get('FABTOOLS_TEST_BOX')
    if not vagrant_box:
        pytest.skip("Set FABTOOLS_TEST_BOX to choose a Vagrant base box for functional tests")
    vagrant_provider = os.environ.get('FABTOOLS_TEST_PROVIDER')
    reuse_vm = os.environ.get('FABTOOLS_TEST_REUSE_VM')
    _configure_logging()
    _allow_fabric_to_access_the_real_stdin()
    if not reuse_vm:
        _stop_vagrant_machine()
    _init_vagrant_machine(vagrant_box)
    _start_vagrant_machine(vagrant_provider)
    _target_vagrant_machine()
    _set_optional_http_proxy()
    _update_package_index()
    yield
    if not reuse_vm:
        _stop_vagrant_machine()


def _check_vagrant_version():
    if VAGRANT_VERSION is None:
        pytest.skip("Vagrant is required for functional tests")
    elif VAGRANT_VERSION < MIN_VAGRANT_VERSION:
        pytest.skip("Vagrant >= %s is required for functional tests" % ".".join(map(str, MIN_VAGRANT_VERSION)))


def _configure_logging():
    logger = logging.getLogger('paramiko')
    logger.setLevel(logging.WARN)


def _allow_fabric_to_access_the_real_stdin():
    patcher = patch('fabric.io.sys')
    mock_sys = patcher.start()
    mock_sys.stdin = sys.__stdin__


_VAGRANTFILE_TEMPLATE = """\
Vagrant.configure(2) do |config|

  config.vm.box = "%s"

  # Speed up downloads using a shared cache across boxes
  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box
  end

end
"""


def _init_vagrant_machine(base_box):
    path = os.path.join(HERE, 'Vagrantfile')
    contents = _VAGRANTFILE_TEMPLATE % base_box
    with open(path, 'w') as vagrantfile:
        vagrantfile.write(contents)


def _start_vagrant_machine(provider):
    if provider:
        options = ' --provider %s' % quote(provider)
    else:
        options = ''
    with lcd(HERE):
        with settings(hide('stdout')):
            local('vagrant up' + options)


def _stop_vagrant_machine():
    with lcd(HERE):
        with settings(hide('stdout', 'stderr', 'warnings'), warn_only=True):
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
    env.abort_on_prompts = True


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
        from fabtools.require.deb import uptodate_index
        uptodate_index()


@pytest.fixture(scope='session', autouse=True)
def allow_sudo_user(setup_package):
    """
    Fix sudo config if needed

    Some Vagrant boxes come with a too restrictive sudoers config
    and only allow the vagrant user to run commands as root.
    """
    from fabtools.require import file as require_file
    require_file(
        '/etc/sudoers.d/fabtools',
        contents="vagrant ALL=(ALL) NOPASSWD:ALL\n",
        owner='root',
        mode='440',
        use_sudo=True,
    )
