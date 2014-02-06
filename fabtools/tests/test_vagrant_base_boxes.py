import textwrap
import unittest

from mock import patch


class TestParseVagrantMachineReadableBoxList(unittest.TestCase):

    def test_machine_readable_box_list(self):
        with patch('fabtools.vagrant.local') as mock_local:
            mock_local.return_value = textwrap.dedent(r"""
                1391708688,,box-name,lucid32
                1391708688,,box-provider,virtualbox
                1391708688,,box-name,precise64
                1391708688,,box-provider,virtualbox
                1391708688,,box-name,precise64
                1391708688,,box-provider,vmware_fusion
                """)
            from fabtools.vagrant import _box_list_machine_readable
            res = _box_list_machine_readable()
            self.assertEqual(res, [
                ('lucid32', 'virtualbox'),
                ('precise64', 'virtualbox'),
                ('precise64', 'vmware_fusion'),
            ])


class TestParseVagrantBoxListWithProvider(unittest.TestCase):

    def test_parse_box_list(self):
        with patch('fabtools.vagrant.local') as mock_local:
            mock_local.return_value = textwrap.dedent("""\
                lucid32                   (virtualbox)
                precise64                 (virtualbox)
                precise64                 (vmware_fusion)
                """)
            from fabtools.vagrant import _box_list_human_readable
            res = _box_list_human_readable()
            self.assertEqual(res, [
                ('lucid32', 'virtualbox'),
                ('precise64', 'virtualbox'),
                ('precise64', 'vmware_fusion'),
            ])


class TestParseVagrantBoxListWithoutProvider(unittest.TestCase):

    def test_parse_box_list(self):
        with patch('fabtools.vagrant.local') as mock_local:
            mock_local.return_value = textwrap.dedent("""\
                lucid32
                precise64
                """)
            from fabtools.vagrant import _box_list_human_readable
            res = _box_list_human_readable()
            self.assertEqual(res, [
                ('lucid32', 'virtualbox'),
                ('precise64', 'virtualbox'),
            ])


class TestVagrantBaseBoxes(unittest.TestCase):

    def test_vagrant_base_boxes(self):
        with patch('fabtools.vagrant._box_list') as mock_list:
            mock_list.return_value = [
                ('lucid32', 'virtualbox'),
                ('precise64', 'virtualbox'),
                ('precise64', 'vmware_fusion'),
            ]
            from fabtools.vagrant import base_boxes
            self.assertEqual(base_boxes(), ['lucid32', 'precise64'])
