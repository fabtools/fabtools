from __future__ import with_statement
from contextlib import closing

import unittest
import os
from fabtools.cron import CrontabManager

CRON_D = os.path.join(os.path.dirname(__file__), 'cron.d')


class TestEmptyCrontabManager(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(CRON_D, 'empty_cron'), 'w') as f:
            f.write('')

    def test_read(self):
        cm = CrontabManager(os.path.join(CRON_D, 'empty_cron'))
        cm.read_crontab()
        self.assertEquals([], cm.crontab)

    def test_find_boundaries(self):
        cm = CrontabManager(os.path.join(CRON_D, 'empty_cron'))
        cm.read_crontab()
        self.assertEquals((None, None), cm.find_boundaries('test'))

    def test_has_entry(self):
        cm = CrontabManager(os.path.join(CRON_D, 'empty_cron'))
        cm.read_crontab()
        self.assertFalse(cm.has_entry('test'))

    def test_del_entry(self):
        '''
        Test that removing a non existing entry is harmless.
        '''
        cm = CrontabManager(os.path.join(CRON_D, 'empty_cron'))
        cm.read_crontab()
        self.assertEquals(0, cm.del_entry('test'))

    def test_add_write(self):
        name = 'test'
        entry = '0 */2 * * * username /home/username/test.pl'
        cm = CrontabManager(os.path.join(CRON_D, 'empty_cron'))
        cm.read_crontab()
        cm.add_entry(name, entry)
        crontab = ['', cm.prepend % name, entry, cm.append % name]
        self.assertEquals(cm.crontab, crontab)
        cm.write_crontab()
        with closing(open(cm._path)) as f:
            self.assertEquals('\n'.join(crontab) + '\n', f.read())

    def tearDown(self):
        os.unlink(os.path.join(CRON_D, 'empty_cron'))


class TestExistingCrontabManager(unittest.TestCase):

    def test_has_entry(self):
        cm = CrontabManager(os.path.join(CRON_D, 'test_cron'))
        cm.read_crontab()
        self.assertTrue(cm.has_entry('test'))

    def test_del_entry(self):
        cm = CrontabManager(os.path.join(CRON_D, 'test_cron'))
        cm.read_crontab()
        self.assertEquals(1, cm.del_entry('test'))

    def test_find_boundaries(self):
        cm = CrontabManager(os.path.join(CRON_D, 'test_cron'))
        cm.read_crontab()
        self.assertEquals((1, 4), cm.find_boundaries('test'))

    def test_add(self):
        '''
        Test that adding the same item is harmless.
        '''
        name = 'test'
        entry = '0 */2 * * * username /home/username/test.pl'
        cm = CrontabManager(os.path.join(CRON_D, 'test_cron'))
        cm.read_crontab()
        cm.add_entry(name, entry)
        crontab = ['', cm.prepend % name, entry, cm.append % name]
        self.assertEquals(cm.crontab, crontab)


class TestBrokenCrontabManager(unittest.TestCase):

    def test_find_test(self):
        cm = CrontabManager(os.path.join(CRON_D, 'broken_cron'))
        cm.read_crontab()
        self.assertRaises(RuntimeError, cm.find_boundaries, 'test')

    def test_find_test2(self):
        cm = CrontabManager(os.path.join(CRON_D, 'broken_cron'))
        cm.read_crontab()
        self.assertRaises(RuntimeError, cm.find_boundaries, 'test2')
