#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement

from fabric.api import task
from fabtools import require


@task
def should_verify_tomcat_version():
    """
    Test high level API
    """

    # from fabtools import tomcat
    from fabtools import oracle_jdk,tomcat
    from fabtools.files import is_file

    # Install java and tomcat
    require.oracle_jdk.installed()
    require.tomcat.installed()

    assert is_file('/usr/share/tomcat7/bin/catalina.sh')
    assert tomcat.DEFAULT_VERSION == tomcat.version()