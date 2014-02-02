from __future__ import with_statement

from textwrap import dedent

from fabric.api import (
    quiet,
    # run,
)
from fabric.contrib.files import contains


from fabtools.require import file as require_file
from fabtools.tests.vagrant_test_case import VagrantTestCase


SSHD_CONFIG = '/tmp/sshd_config'


SSHD_CONFIG_CONTENTS = [
    """
    """,

    """
    PasswordAuthentication yes
    PermitRootLogin yes
    """,

    """
    PasswordAuthentication yes
    PermitRootLogin no
    """,

    """
    PasswordAuthentication no
    PermitRootLogin yes
    """,

    """
    PasswordAuthentication no
    PermitRootLogin no
    """,
]


class TestSSHHardening(VagrantTestCase):
    """
    Test SSH hardening operations
    """

    def test_disable_password_auth(self):

        def check_disable_password_auth(contents):
            from fabtools.ssh import disable_password_auth
            require_file(SSHD_CONFIG, contents=contents)
            disable_password_auth(sshd_config=SSHD_CONFIG)
            with quiet():
                assert contains(SSHD_CONFIG, 'PasswordAuthentication no', exact=True)
                assert not contains(SSHD_CONFIG, 'PasswordAuthentication yes', exact=True)

        for contents in SSHD_CONFIG_CONTENTS:
            yield check_disable_password_auth, dedent(contents)

    def test_disable_root_login(self):

        def check_disable_root_login(contents):
            from fabtools.ssh import disable_root_login
            require_file(SSHD_CONFIG, contents=contents)
            disable_root_login(sshd_config=SSHD_CONFIG)
            with quiet():
                assert contains(SSHD_CONFIG, 'PermitRootLogin no', exact=True)
                assert not contains(SSHD_CONFIG, 'PermitRootLogin yes', exact=True)

        for contents in SSHD_CONFIG_CONTENTS:
            yield check_disable_root_login, dedent(contents)

    def test_enable_password_auth(self):

        def check_enable_password_auth(contents):
            from fabtools.ssh import enable_password_auth
            require_file(SSHD_CONFIG, contents=contents)
            enable_password_auth(sshd_config=SSHD_CONFIG)
            with quiet():
                assert contains(SSHD_CONFIG, 'PasswordAuthentication yes', exact=True)
                assert not contains(SSHD_CONFIG, 'PasswordAuthentication no', exact=True)

        for contents in SSHD_CONFIG_CONTENTS:
            yield check_enable_password_auth, dedent(contents)

    def test_enable_root_login(self):

        def check_enable_root_login(contents):
            from fabtools.ssh import enable_root_login
            require_file(SSHD_CONFIG, contents=contents)
            enable_root_login(sshd_config=SSHD_CONFIG)
            with quiet():
                assert contains(SSHD_CONFIG, 'PermitRootLogin yes', exact=True)
                assert not contains(SSHD_CONFIG, 'PermitRootLogin no', exact=True)

        for contents in SSHD_CONFIG_CONTENTS:
            yield check_enable_root_login, dedent(contents)
