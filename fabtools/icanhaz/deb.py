"""
Idempotent API for managing Debian/Ubuntu packages
"""
from fabtools.deb import *


def package(pkg_name, update=False):
    """
    I can haz deb package
    """
    if not is_installed(pkg_name):
        install(pkg_name, update)


def packages(pkg_list, update=False):
    """
    I can haz several deb packages
    """
    pkg_list = [pkg for pkg in pkg_list if not is_installed(pkg)]
    install(pkg_list, update)
