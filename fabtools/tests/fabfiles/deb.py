from __future__ import with_statement

from fabric.api import (
    hide,
    run,
    settings,
    task,
)
from fabtools.utils import run_as_root


def reset():
    with settings(hide('output', 'warnings'), warn_only=True):
        run_as_root('apt-key del 7BD9BF62')
        run_as_root('apt-key del C4DEFFEB')


@task
def test_add_apt_key_with_key_id_from_url():
    from fabtools.deb import add_apt_key
    reset()
    add_apt_key(keyid='C4DEFFEB', url='http://repo.varnish-cache.org/debian/GPG-key.txt')
    run_as_root('apt-key finger | grep -q C4DEFFEB')


@task
def test_add_apt_key_with_key_id_from_specific_key_server():
    from fabtools.deb import add_apt_key
    reset()
    add_apt_key(keyid='7BD9BF62', keyserver='keyserver.ubuntu.com')
    run_as_root('apt-key finger | grep -q 7BD9BF62')


@task
def test_add_apt_key_with_key_id_from_file():
    from fabtools.deb import add_apt_key
    reset()
    run('wget http://repo.varnish-cache.org/debian/GPG-key.txt -O /tmp/tmp.fabtools.test.key')
    add_apt_key(keyid='C4DEFFEB', filename='/tmp/tmp.fabtools.test.key')
    run_as_root('apt-key finger | grep -q C4DEFFEB')


@task
def test_add_apt_key_without_key_id_from_url():
    from fabtools.deb import add_apt_key
    reset()
    add_apt_key(url='http://repo.varnish-cache.org/debian/GPG-key.txt')
    run_as_root('apt-key finger | grep -q C4DEFFEB')


@task
def test_add_apt_key_without_key_id_from_file():
    from fabtools.deb import add_apt_key
    reset()
    run('wget http://repo.varnish-cache.org/debian/GPG-key.txt -O /tmp/tmp.fabtools.test.key')
    add_apt_key(filename='/tmp/tmp.fabtools.test.key')
    run_as_root('apt-key finger | grep -q C4DEFFEB')


@task
def test_require_deb_key_from_url():
    from fabtools.require.deb import key as require_key
    reset()
    require_key(keyid='C4DEFFEB', url='http://repo.varnish-cache.org/debian/GPG-key.txt')
    run_as_root('apt-key finger | grep -q C4DEFFEB')


@task
def test_require_deb_key_from_specific_keyserver():
    from fabtools.require.deb import key as require_key
    reset()
    require_key(keyid='7BD9BF62', keyserver='keyserver.ubuntu.com')
    run_as_root('apt-key finger | grep -q 7BD9BF62')


@task
def test_require_deb_key_from_file():
    from fabtools.require.deb import key as require_key
    reset()
    run('wget http://repo.varnish-cache.org/debian/GPG-key.txt -O /tmp/tmp.fabtools.test.key')
    require_key(keyid='C4DEFFEB', filename='/tmp/tmp.fabtools.test.key')
    run_as_root('apt-key finger | grep -q C4DEFFEB')
