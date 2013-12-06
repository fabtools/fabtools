import unittest

import mock


class CreateGroupTestCase(unittest.TestCase):

    @mock.patch('fabtools.group.run_as_root')
    def test_gid_str(self, mock_run_as_root):
        from fabtools.group import create
        create('some_group', gid='421')

    @mock.patch('fabtools.group.run_as_root')
    def test_gid_int(self, mock_run_as_root):
        from fabtools.group import create
        create('some_group', gid=421)
