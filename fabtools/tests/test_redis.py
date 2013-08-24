import unittest


class RedisTestCase(unittest.TestCase):

    def test_parse_version(self):

        from fabtools.require.redis import _parse_version

        self.assertEqual(
            _parse_version('2.6.14'),
            (2, 6, 14)
        )

    def test_old_download_url(self):

        from fabtools.require.redis import _download_url

        self.assertEqual(
            _download_url('2.6.14'),
            'http://redis.googlecode.com/files/'
        )

    def test_new_download_url(self):

        from fabtools.require.redis import _download_url

        self.assertEqual(
            _download_url('2.6.15'),
            'http://download.redis.io/releases/'
        )
