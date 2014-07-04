"""
Tomcat
============

This module provides tools for installing `Tomcat`_

.. _Tomcat: http://tomcat.apache.org

"""

from fabtools import tomcat


def installed(version=tomcat.DEFAULT_VERSION):
    """
    Require Tomcat to be installed.

    ::

        from fabtools import require

        require.tomcat.installed()

    """
    if tomcat.version(tomcat.DEFAULT_INSTALLATION_PATH) != version:
        tomcat.install_from_source(version=version, overwrite=True)
