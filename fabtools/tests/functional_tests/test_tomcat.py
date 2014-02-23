import os

import pytest

from fabtools.files import is_file


pytestmark = pytest.mark.network


PATH = "/usr/share/tomcat"


@pytest.fixture(scope='module')
def jdk():
    from fabtools.require.oracle_jdk import installed
    installed()


def test_tomcat_7_version(jdk):

    from fabtools.require.tomcat import installed
    from fabtools.tomcat import version, DEFAULT_VERSION

    installed()

    assert is_file(os.path.join(PATH, 'bin/catalina.sh'))
    assert version(PATH) == DEFAULT_VERSION


def test_tomcat_6_version(jdk):

    TOMCAT6_VERSION = '6.0.36'

    from fabtools.require.tomcat import installed
    from fabtools.tomcat import version

    installed(version=TOMCAT6_VERSION)

    assert is_file(os.path.join(PATH, 'bin/catalina.sh'))
    assert version(PATH) == TOMCAT6_VERSION
