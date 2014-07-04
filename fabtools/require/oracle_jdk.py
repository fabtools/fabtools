"""
Oracle JDK
============

This module provides tools for installing `Oracle JDK`_

.. _Oracle JDK: http://www.oracle.com/technetwork/java/javase/

"""

from fabtools import oracle_jdk


def installed(version=oracle_jdk.DEFAULT_VERSION):
    """
    Require Oracle JDK to be installed.

    ::

        from fabtools import require

        require.oracle_jdk.installed()

    """
    if oracle_jdk.version() != version:
        oracle_jdk.install_from_oracle_site(version)
