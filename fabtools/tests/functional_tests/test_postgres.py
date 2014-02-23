import functools

import pytest


pytestmark = pytest.mark.network


@pytest.fixture(scope='module')
def postgres_server():
    from fabtools.require.postgres import server
    server()


@pytest.fixture(scope='module')
def postgres_user(request):
    from fabtools.postgres import drop_user
    from fabtools.require.postgres import user
    name = 'pguser'
    user(name, password='s3cr3t')
    request.addfinalizer(functools.partial(drop_user, name))
    return name


def test_create_and_drop_user(postgres_server):

    from fabtools.postgres import create_user, drop_user, user_exists

    create_user('alice', password='1234')
    assert user_exists('alice')

    drop_user('alice')
    assert not user_exists('alice')


def test_require_user(postgres_server):

    from fabtools.postgres import user_exists, drop_user
    from fabtools.require.postgres import user

    user('bob', password='foo')

    assert user_exists('bob')

    drop_user('bob')


def test_require_database(postgres_server, postgres_user):

    from fabtools.postgres import database_exists, drop_database
    from fabtools.require.postgres import database

    database('pgdb', postgres_user)

    assert database_exists('pgdb')

    drop_database('pgdb')
