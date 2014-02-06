from __future__ import with_statement

import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from fabric.api import env, hide, lcd, local, settings, shell_env
from fabric.state import connections

import fabtools
from fabtools import require
from fabtools.vagrant import base_boxes, status, version


def halt_and_destroy():
    """
    Halt and destoy virtual machine
    """
    with lcd(os.path.dirname(__file__)):
        if os.path.exists(os.path.join(env['lcwd'], 'Vagrantfile')):
            local('vagrant halt')
            if version() >= (0, 9, 99):
                local('vagrant destroy -f')
            else:
                local('vagrant destroy')


def test_boxes():
    """
    Get the list of vagrant base boxes to use

    The default is to get the list of all base boxes.

    This can be overridden with the FABTOOLS_TEST_BOXES environment variable.
    """
    boxes = os.environ.get('FABTOOLS_TEST_BOXES')
    if boxes is not None:
        return boxes.split()
    else:
        return base_boxes()


class VagrantTestSuite(unittest.BaseTestSuite):
    """
    Test suite with vagrant support
    """

    def __init__(self, base_boxes):
        self.base_boxes = base_boxes
        self.current_box = None
        unittest.BaseTestSuite.__init__(self)

    def addTest(self, test):
        test._suite = self
        unittest.BaseTestSuite.addTest(self, test)

    def run(self, result):
        """
        Run the test suite on all the virtual machines
        """
        for base_box in self.base_boxes:

            # Start a virtual machine using this base box
            self.current_box = base_box
            self.start_box()

            # Clear fabric connection cache
            with self.settings():
                if env.host_string in connections:
                    del connections[env.host_string]

            # Make sure the vagrant user can sudo to any user
            with self.settings():
                require.sudoer('vagrant')

            # Make sure the package index is up to date
            with self.settings():
                if fabtools.system.distrib_family() == 'debian':
                    fabtools.deb.update_index()

            # Run the test suite
            unittest.BaseTestSuite.run(self, result)

            # Stop the virtual machine and clean up
            self.stop_box()

    def start_box(self):
        """
        Spin up a new vagrant box
        """

        # Support for Vagrant 1.1 providers
        if ':' in self.current_box:
            box_name, provider = self.current_box.split(':', 1)
        else:
            box_name = self.current_box
            provider = None

        with lcd(os.path.dirname(__file__)):

            if not os.path.exists('Vagrantfile') \
               or not os.environ.get('FABTOOLS_TEST_NODESTROY'):

                # Create a fresh vagrant config file
                local('rm -f Vagrantfile')
                local('vagrant init %s' % box_name)

                # Clean up
                if status() != 'not created':
                    halt_and_destroy()

            if provider:
                options = ' --provider %s' % provider
            else:
                options = ''

            # Spin up the box
            # (retry as it sometimes fails for no good reason)
            cmd = 'vagrant up%s' % options
            local('%s || %s' % (cmd, cmd))

    def ssh_config(self):
        """
        Get SSH connection parameters for the current box
        """
        with lcd(os.path.dirname(__file__)):
            if version() >= (0, 9, 0):
                command = 'ssh-config'
            else:
                command = 'ssh_config'
            with settings(hide('running')):
                output = local('vagrant %s' % command, capture=True)

        config = {}
        for line in output.splitlines()[1:]:
            key, value = line.strip().split(' ', 2)
            config[key] = value
        return config

    def stop_box(self):
        """
        Spin down the vagrant box
        """
        if not os.environ.get('FABTOOLS_TEST_NODESTROY'):
            halt_and_destroy()
            with lcd(os.path.dirname(__file__)):
                local('rm -f Vagrantfile')
        self.current_box = None

    def settings(self, *args, **kwargs):
        """
        Return a Fabric context manager with the right host settings
        """
        config = self.ssh_config()

        user = config['User']
        hostname = config['HostName']
        port = config['Port']

        kwargs['host_string'] = "%s@%s:%s" % (user, hostname, port)
        kwargs['user'] = user
        kwargs['key_filename'] = config['IdentityFile'].strip('"')
        kwargs['disable_known_hosts'] = True

        return settings(*args, **kwargs)


class VagrantTestCase(unittest.TestCase):
    """
    Test case with vagrant support
    """

    def __init__(self, name, callable):
        super(VagrantTestCase, self).__init__()
        self._name = name
        self._callable = callable

    def run(self, result=None):
        """
        Run the test case within a Fabric context manager
        """
        with self._suite.settings():
            http_proxy = os.environ.get('FABTOOLS_HTTP_PROXY', '')
            with shell_env(http_proxy=http_proxy):
                unittest.TestCase.run(self, result)

    def runTest(self):
        self._callable()
