#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement

from fabric.api import *

from fabtools.vagrant import vagrant


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
