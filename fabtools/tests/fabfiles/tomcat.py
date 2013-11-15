#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement

# Standard imports
import os

# Fabric imports
from fabric.api import task
from fabtools import require
from fabtools.tomcat import DEFAULT_VERSION


@task
def should_verify_tomcat_7_version(installation_path="/usr/share/tomcat"):
    """
    Test high level API
    """

    # from fabtools import tomcat
    from fabtools import oracle_jdk, tomcat
    from fabtools.files import is_file

    # Install java and tomcat
    require.oracle_jdk.installed()
    require.tomcat.installed()

    assert is_file(os.path.join(installation_path, 'bin/catalina.sh'))
    assert DEFAULT_VERSION == tomcat.version(installation_path)


@task
def should_verify_tomcat_6_version(installation_path="/usr/share/tomcat"):
    """
    Test high level API
    """
    tomcat6 = '6.0.36'
    # from fabtools import tomcat
    from fabtools import oracle_jdk, tomcat
    from fabtools.files import is_file

    # Install java and tomcat
    require.oracle_jdk.installed()
    require.tomcat.installed(tomcat_version=tomcat6)

    assert is_file(os.path.join(installation_path, 'bin/catalina.sh'))
    assert tomcat6 == tomcat.version(installation_path)
