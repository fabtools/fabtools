from __future__ import with_statement

from textwrap import dedent

from fabric.api import (
    quiet,
    run,
    task,
)
from fabric.contrib.files import contains


@task
def ssh():
    """
    Test SSH hardening operations
    """

    import fabtools

    SSHD_CONFIG = '/tmp/sshd_config'

    SSHD_CONFIG_CONTENT = [
        '''
        ''',

        '''
        PasswordAuthentication yes
        PermitRootLogin yes
        ''',

        '''
        PasswordAuthentication yes
        PermitRootLogin no
        ''',

        '''
        PasswordAuthentication no
        PermitRootLogin yes
        ''',

        '''
        PasswordAuthentication no
        PermitRootLogin no
        ''',
    ]

    def check_disable_password_auth(sshd_config):
        fabtools.ssh.disable_password_auth(sshd_config=sshd_config)
        with quiet():
            assert contains(sshd_config, 'PasswordAuthentication no', exact=True)
            assert not contains(sshd_config, 'PasswordAuthentication yes', exact=True)

    def check_disable_root_login(sshd_config):
        fabtools.ssh.disable_root_login(sshd_config=sshd_config)
        with quiet():
            assert contains(sshd_config, 'PermitRootLogin no', exact=True)
            assert not contains(sshd_config, 'PermitRootLogin yes', exact=True)

    def check_enable_password_auth(sshd_config):
        fabtools.ssh.enable_password_auth(sshd_config=sshd_config)
        with quiet():
            assert contains(sshd_config, 'PasswordAuthentication yes', exact=True)
            assert not contains(sshd_config, 'PasswordAuthentication no', exact=True)

    def check_enable_root_login(sshd_config):
        fabtools.ssh.enable_root_login(sshd_config=sshd_config)
        with quiet():
            assert contains(sshd_config, 'PermitRootLogin yes', exact=True)
            assert not contains(sshd_config, 'PermitRootLogin no', exact=True)

    for content in SSHD_CONFIG_CONTENT:

        run('rm -f %s' % SSHD_CONFIG)
        fabtools.require.file(SSHD_CONFIG, contents=dedent(content))

        check_disable_password_auth(SSHD_CONFIG)
        check_disable_root_login(SSHD_CONFIG)
        check_enable_password_auth(SSHD_CONFIG)
        check_enable_root_login(SSHD_CONFIG)

    for content in SSHD_CONFIG_CONTENT:

        run('rm -f %s' % SSHD_CONFIG)
        fabtools.require.file(SSHD_CONFIG, contents=dedent(content))

        check_enable_password_auth(SSHD_CONFIG)
        check_enable_root_login(SSHD_CONFIG)
        check_disable_password_auth(SSHD_CONFIG)
        check_disable_root_login(SSHD_CONFIG)
