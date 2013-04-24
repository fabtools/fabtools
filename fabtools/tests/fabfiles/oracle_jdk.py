#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement

from fabric.api import task


@task
def require_oracle_jdk():
    """
    Test high level API
    """

    from fabtools import oracle_jdk
    from fabtools import require
    from fabtools.files import is_file

    # Require Oracle JDK

    require.oracle_jdk.installed()

    assert is_file('/opt/jdk/bin/java')
    assert oracle_jdk.version() == oracle_jdk.DEFAULT_VERSION

    # Require Oracle JDK version 6
    require.oracle_jdk.installed('6u45-b06')

    assert is_file('/opt/jdk/bin/java')
    assert oracle_jdk.version() == '6u45-b06'
