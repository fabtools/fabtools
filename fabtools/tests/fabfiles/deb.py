from __future__ import with_statement

from fabric.api import (
    run,
    task,
)


def reset():
    from fabric.api import settings
    from fabtools.utils import run_as_root

    with settings(warn_only=True):
        run_as_root('apt-key del 7BD9BF62')
        run_as_root('apt-key del C4DEFFEB')


@task
def deb():
    """
    Check deb functions.
    """

    from fabtools import require
    from fabtools import deb
    from fabtools.utils import run_as_root

    # deb.add_apt_key with keyid
    reset()
    deb.add_apt_key(keyid='C4DEFFEB', url='http://repo.varnish-cache.org/debian/GPG-key.txt')
    run_as_root('apt-key finger | grep -q C4DEFFEB')

    reset()
    deb.add_apt_key(keyid='7BD9BF62')
    deb.add_apt_key(keyid='7BD9BF62') # Intentionally repeated
    run_as_root('apt-key finger | grep -q 7BD9BF62')

    reset()
    deb.add_apt_key(keyid='7BD9BF62', keyserver='keyserver.ubuntu.com')
    run_as_root('apt-key finger | grep -q 7BD9BF62')

    reset()
    run('wget http://repo.varnish-cache.org/debian/GPG-key.txt -O /tmp/tmp.fabtools.test.key')
    deb.add_apt_key(keyid='C4DEFFEB', filename='/tmp/tmp.fabtools.test.key')
    run_as_root('apt-key finger | grep -q C4DEFFEB')


    # deb.add_apt_key without keyid
    reset()
    deb.add_apt_key(url='http://repo.varnish-cache.org/debian/GPG-key.txt')
    run_as_root('apt-key finger | grep -q C4DEFFEB')

    reset()
    deb.add_apt_key(keyid='7BD9BF62')
    run_as_root('apt-key finger | grep -q 7BD9BF62')

    reset()
    run('wget http://repo.varnish-cache.org/debian/GPG-key.txt -O /tmp/tmp.fabtools.test.key')
    deb.add_apt_key(filename='/tmp/tmp.fabtools.test.key')
    run_as_root('apt-key finger | grep -q C4DEFFEB')

    # require.deb.key
    reset()
    require.deb.key(keyid='C4DEFFEB', url='http://repo.varnish-cache.org/debian/GPG-key.txt')
    run_as_root('apt-key finger | grep -q C4DEFFEB')

    reset()
    require.deb.key(keyid='7BD9BF62')
    require.deb.key(keyid='7BD9BF62') # Intentionally repeated
    run_as_root('apt-key finger | grep -q 7BD9BF62')

    reset()
    require.deb.key(keyid='7BD9BF62', keyserver='keyserver.ubuntu.com')
    run_as_root('apt-key finger | grep -q 7BD9BF62')

    reset()
    run('wget http://repo.varnish-cache.org/debian/GPG-key.txt -O /tmp/tmp.fabtools.test.key')
    require.deb.key(keyid='C4DEFFEB', filename='/tmp/tmp.fabtools.test.key')
    run_as_root('apt-key finger | grep -q C4DEFFEB')


