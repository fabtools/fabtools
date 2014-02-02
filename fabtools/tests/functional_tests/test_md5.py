from __future__ import with_statement

import hashlib

from fabric.api import hide, run, settings

from fabtools.tests.vagrant_test_case import VagrantTestCase
import fabtools


class TestMD5Sum(VagrantTestCase):
    """
    Check MD5 sums
    """

    def test_md5sum_empty_file(self):
        run('touch f1')
        expected_hash = hashlib.md5('').hexdigest()
        self.assertEqual(fabtools.files.md5sum('f1'), expected_hash)
        run('rm -f f1')

    def test_md5sum(self):
        run('echo -n hello > f2')
        expected_hash = hashlib.md5('hello').hexdigest()
        self.assertEqual(fabtools.files.md5sum('f2'), expected_hash)
        run('rm -f f2')

    def test_md5sum_not_existing_file(self):
        with settings(hide('warnings')):
            self.assertIsNone(fabtools.files.md5sum('doesnotexist'))
