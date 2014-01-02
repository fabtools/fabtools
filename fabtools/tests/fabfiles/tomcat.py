#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement

import os

from fabric.api import task

from fabtools import require, tomcat
from fabtools.files import is_file


@task
def should_verify_tomcat_7_version(path="/usr/share/tomcat"):
    """
    Test high level API
    """

    require.oracle_jdk.installed()
    require.tomcat.installed()

    assert is_file(os.path.join(path, 'bin/catalina.sh'))
    assert tomcat.DEFAULT_VERSION == tomcat.version(path)


@task
def should_verify_tomcat_6_version(path="/usr/share/tomcat"):
    """
    Test high level API
    """
    tomcat6 = '6.0.36'

    require.oracle_jdk.installed()
    require.tomcat.installed(version=tomcat6)

    assert is_file(os.path.join(path, 'bin/catalina.sh'))
    assert tomcat6 == tomcat.version(path)
