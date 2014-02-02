from __future__ import with_statement

from fabric.api import (
    hide,
    run,
    settings,
)
from fabtools.utils import run_as_root

from fabtools.tests.vagrant_test_case import VagrantTestCase


class TestAPTKey(VagrantTestCase):

    def setUp(self):
        with settings(hide('output', 'warnings'), warn_only=True):
            run_as_root('apt-key del 7BD9BF62')
            run_as_root('apt-key del C4DEFFEB')

    def test_add_apt_key_with_key_id_from_url(self):
        from fabtools.deb import add_apt_key
        add_apt_key(keyid='C4DEFFEB', url='http://repo.varnish-cache.org/debian/GPG-key.txt')
        run_as_root('apt-key finger | grep -q C4DEFFEB')

    def test_add_apt_key_with_key_id_from_specific_key_server(self):
        from fabtools.deb import add_apt_key
        add_apt_key(keyid='7BD9BF62', keyserver='keyserver.ubuntu.com')
        run_as_root('apt-key finger | grep -q 7BD9BF62')

    def test_add_apt_key_with_key_id_from_file(self):
        from fabtools.deb import add_apt_key
        run('wget http://repo.varnish-cache.org/debian/GPG-key.txt -O /tmp/tmp.fabtools.test.key')
        add_apt_key(keyid='C4DEFFEB', filename='/tmp/tmp.fabtools.test.key')
        run_as_root('apt-key finger | grep -q C4DEFFEB')

    def test_add_apt_key_without_key_id_from_url(self):
        from fabtools.deb import add_apt_key
        add_apt_key(url='http://repo.varnish-cache.org/debian/GPG-key.txt')
        run_as_root('apt-key finger | grep -q C4DEFFEB')

    def test_add_apt_key_without_key_id_from_file(self):
        from fabtools.deb import add_apt_key
        run('wget http://repo.varnish-cache.org/debian/GPG-key.txt -O /tmp/tmp.fabtools.test.key')
        add_apt_key(filename='/tmp/tmp.fabtools.test.key')
        run_as_root('apt-key finger | grep -q C4DEFFEB')

    def test_require_deb_key_from_url(self):
        from fabtools.require.deb import key as require_key
        require_key(keyid='C4DEFFEB', url='http://repo.varnish-cache.org/debian/GPG-key.txt')
        run_as_root('apt-key finger | grep -q C4DEFFEB')

    def test_require_deb_key_from_specific_keyserver(self):
        from fabtools.require.deb import key as require_key
        require_key(keyid='7BD9BF62', keyserver='keyserver.ubuntu.com')
        run_as_root('apt-key finger | grep -q 7BD9BF62')

    def test_require_deb_key_from_file(self):
        from fabtools.require.deb import key as require_key
        run('wget http://repo.varnish-cache.org/debian/GPG-key.txt -O /tmp/tmp.fabtools.test.key')
        require_key(keyid='C4DEFFEB', filename='/tmp/tmp.fabtools.test.key')
        run_as_root('apt-key finger | grep -q C4DEFFEB')
