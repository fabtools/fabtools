import pytest

from fabric.api import run

from fabtools.files import is_file


pytestmark = pytest.mark.network


@pytest.fixture
def redis():
    from fabtools.require.redis import installed_from_source
    installed_from_source()


@pytest.fixture
def instance():
    from fabtools.require.redis import instance
    instance('db1', port='6379')


def test_redis_server_is_installed(redis):
    from fabtools.require.redis import VERSION
    assert is_file('/opt/redis-%s/redis-server' % VERSION)


def test_save_rdb_file(redis, instance):
    from fabtools.require.redis import VERSION
    res = run('echo SAVE | /opt/redis-%s/redis-cli' % VERSION)
    assert res == 'OK'
