import textwrap
import unittest

from mock import patch


class TestParseVagrantMachineReadableStatus(unittest.TestCase):

    def test_machine_readable_status_running(self):
        with patch('fabtools.vagrant.local') as mock_local:
            mock_local.return_value = textwrap.dedent(r"""
                1391354677,default,provider-name,vmware_fusion
                1391354677,default,state,running
                1391354677,default,state-human-short,running
                1391354677,default,state-human-long,The VM is running. To stop this VM%!(VAGRANT_COMMA) you can run `vagrant halt` to\nshut it down%!(VAGRANT_COMMA) or you can run `vagrant suspend` to simply suspend\nthe virtual machine. In either case%!(VAGRANT_COMMA) to restart it again%!(VAGRANT_COMMA) run\n`vagrant up`.
                """)
            from fabtools.vagrant import _status_machine_readable
            res = _status_machine_readable()
            self.assertEqual(res, [('default', 'running')])

    def test_machine_readable_status_not_running(self):
        with patch('fabtools.vagrant.local') as mock_local:
            mock_local.return_value = textwrap.dedent(r"""
                1391366299,default,provider-name,vmware_fusion
                1391366299,default,state,not_running
                1391366299,default,state-human-short,not running
                1391366299,default,state-human-long,The VM is powered off. To restart the VM%!(VAGRANT_COMMA) run `vagrant up`
                """)
            from fabtools.vagrant import _status_machine_readable
            res = _status_machine_readable()
            self.assertEqual(res, [('default', 'not running')])


class TestParseVagrantStatusWithProvider(unittest.TestCase):

    def test_parse_status_running(self):
        with patch('fabtools.vagrant.local') as mock_local:
            mock_local.return_value = textwrap.dedent("""\
                Current machine states:

                default                   running (vmware_fusion)

                The VM is running. To stop this VM, you can run `vagrant halt` to
                shut it down, or you can run `vagrant suspend` to simply suspend
                the virtual machine. In either case, to restart it again, run
                `vagrant up`.
                """)
            from fabtools.vagrant import _status_human_readable
            res = _status_human_readable()
            self.assertEqual(res, [('default', 'running')])

    def test_parse_status_not_created(self):
        with patch('fabtools.vagrant.local') as mock_local:
            mock_local.return_value = textwrap.dedent("""\
                Current machine states:

                default                   not created (vmware_fusion)

                The VMware machine has not yet been created. Run `vagrant up`
                to create the machine. If a machine is not created, only the
                default provider will be shown. Therefore, if a provider is not listed,
                then the machine is not created for that provider.
                """)
            from fabtools.vagrant import _status_human_readable
            res = _status_human_readable()
            self.assertEqual(res, [('default', 'not created')])


class TestParseVagrantStatusWithoutProvider(unittest.TestCase):

    def test_parse_status_running(self):
        with patch('fabtools.vagrant.local') as mock_local:
            mock_local.return_value = textwrap.dedent("""\
                Current machine states:

                default                   running

                The VM is running. To stop this VM, you can run `vagrant halt` to
                shut it down, or you can run `vagrant suspend` to simply suspend
                the virtual machine. In either case, to restart it again, run
                `vagrant up`.
                """)
            from fabtools.vagrant import _status_human_readable
            res = _status_human_readable()
            self.assertEqual(res, [('default', 'running')])

    def test_parse_status_not_created(self):
        with patch('fabtools.vagrant.local') as mock_local:
            mock_local.return_value = textwrap.dedent("""\
                Current machine states:

                default                   not created

                The VMware machine has not yet been created. Run `vagrant up`
                to create the machine. If a machine is not created, only the
                default provider will be shown. Therefore, if a provider is not listed,
                then the machine is not created for that provider.
                """)
            from fabtools.vagrant import _status_human_readable
            res = _status_human_readable()
            self.assertEqual(res, [('default', 'not created')])


class TestVagrantStatus(unittest.TestCase):

    def test_status(self):
        with patch('fabtools.vagrant._status') as mock_status:
            mock_status.return_value = [('default', 'running')]
            from fabtools.vagrant import status
            self.assertEqual(status(), 'running')
