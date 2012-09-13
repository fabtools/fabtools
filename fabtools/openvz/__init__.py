"""
OpenVZ containers
=================

This module provides high-level tools for managing OpenVZ_ templates
and containers.

.. _OpenVZ: http://openvz.org/

.. warning:: The remote host needs a patched kernel with OpenVZ support.

"""
from fabtools.openvz.operations import *
from fabtools.openvz.contextmanager import guest
