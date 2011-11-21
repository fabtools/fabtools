import os.path

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from fabric.api import *
from fabric.state import connections

from fabtools import require


class VagrantTestSuite(unittest.TestSuite):
    """
    Test suite with vagrant support
    """

    def __init__(self, base_boxes):
        self.base_boxes = base_boxes
        self.current_box = None
        unittest.TestSuite.__init__(self)

    def addTest(self, test):
        test._suite = self
        unittest.TestSuite.addTest(self, test)

    def run(self, result):
        """
        Run the test suite on all the virtual machines
        """
        # Clean up
        with lcd(os.path.dirname(__file__)):
            local('vagrant halt')
            local('vagrant destroy')

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

            # Run the test suite
            unittest.TestSuite.run(self, result)

            # Stop the virtual machine and clean up
            self.stop_box()

    def start_box(self):
        """
        Spin up a new vagrant box
        """
        with lcd(os.path.dirname(__file__)):

            # Create a fresh vagrant config file
            local('rm -f Vagrantfile')
            local('vagrant init %s' % self.current_box)

            # Spin up the box
            local('vagrant up')

    def ssh_config(self):
        """
        Get SSH connection parameters for the current box
        """
        with lcd(os.path.dirname(__file__)):
            output = local('vagrant ssh_config', capture=True)

        config = {}
        for line in output.splitlines()[1:]:
            key, value = line.strip().split(' ', 2)
            config[key] = value
        return config

    def stop_box(self):
        """
        Spin down the vagrant box
        """
        with lcd(os.path.dirname(__file__)):
            local('vagrant halt')
            local('vagrant destroy')
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
        kwargs['key_filename'] = config['IdentityFile']
        kwargs['disable_known_hosts'] = True

        return settings(*args, **kwargs)


class VagrantTestCase(unittest.TestCase):
    """
    Test case with vagrant support
    """

    def run(self, result=None):
        """
        Run the test case within a Fabric context manager
        """
        with self._suite.settings():
            unittest.TestCase.run(self, result)


class VagrantFunctionTestCase(unittest.FunctionTestCase):
    """
    Function test case with vagrant support
    """

    def run(self, result=None):
        """
        Run the test case within a Fabric context manager
        """
        with self._suite.settings():
            unittest.FunctionTestCase.run(self, result)
