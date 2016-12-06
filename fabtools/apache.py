"""
Apache
======

This module provides tools for configuring
the `Apache HTTP Server <http://httpd.apache.org/>`_.

"""

from distutils.version import StrictVersion as V
import posixpath

from fabtools.files import is_link
from fabtools.system import (
    UnsupportedFamily, distrib_family, distrib_id, distrib_release)
from fabtools.utils import run_as_root


def is_module_enabled(module):
    """
    Check if an Apache module is enabled.
    """
    return is_link('/etc/apache2/mods-enabled/%s.load' % module)


def enable_module(module):
    """
    Enable an Apache module.

    This creates a symbolic link from ``/etc/apache2/mods-available/``
    into ``/etc/apache2/mods-enabled/``.

    This does not cause Apache to reload its configuration.

    ::

        import fabtools

        fabtools.apache.enable_module('rewrite')
        fabtools.service.reload('apache2')

    .. seealso:: :py:func:`fabtools.require.apache.module_enabled`
    """
    if not is_module_enabled(module):
        run_as_root('a2enmod %s' % module)


def disable_module(module):
    """
    Disable an Apache module.

    This deletes the symbolink link in ``/etc/apache2/mods-enabled/``.

    This does not cause Apache to reload its configuration.

    ::

        import fabtools

        fabtools.apache.disable_module('rewrite')
        fabtools.service.reload('apache2')

    .. seealso:: :py:func:`fabtools.require.apache.module_disabled`
    """
    if is_module_enabled(module):
        run_as_root('a2dismod %s' % module)


def is_site_enabled(site_name):
    """
    Check if an Apache site is enabled.
    """
    return is_link(_site_link_path(site_name))


def enable_site(site_name):
    """
    Enable an Apache site.

    This creates a symbolic link from ``/etc/apache2/sites-available/``
    into ``/etc/apache2/sites-enabled/``.

    This does not cause Apache to reload its configuration.

    ::

        import fabtools

        fabtools.apache.enable_site('default')
        fabtools.service.reload('apache2')

    .. seealso:: :py:func:`fabtools.require.apache.site_enabled`
    """
    if not is_site_enabled(site_name):
        run_as_root('a2ensite %s' % _site_config_filename(site_name))


def disable_site(site_name):
    """
    Disable an Apache site.

    This deletes the symbolink link in ``/etc/apache2/sites-enabled/``.

    This does not cause Apache to reload its configuration.

    ::

        import fabtools

        fabtools.apache.disable_site('default')
        fabtools.service.reload('apache2')

    .. seealso:: :py:func:`fabtools.require.apache.site_disabled`
    """
    if is_site_enabled(site_name):
        run_as_root('a2dissite %s' % _site_config_filename(site_name))


def _site_config_path(site_name):
    config_filename = _site_config_filename(site_name)
    return posixpath.join('/etc/apache2/sites-available', config_filename)


def _site_config_filename(site_name):
    if site_name == 'default':
        return _default__site_config_filename()
    else:
        return '{0}.conf'.format(site_name)


def _site_link_path(site_name):
    link_filename = _site_link_filename(site_name)
    return posixpath.join('/etc/apache2/sites-enabled', link_filename)


def _site_link_filename(site_name):
    if site_name == 'default':
        return _default__site_link_filename()
    else:
        return '{0}.conf'.format(site_name)


def _default__site_config_filename():
    return _choose(old_style='default', new_style='000-default.conf')


def _default__site_link_filename():
    return _choose(old_style='000-default', new_style='000-default.conf')


def _choose(old_style, new_style):
    family = distrib_family()
    if family == 'debian':
        distrib = distrib_id()
        at_least_trusty = (
            distrib == 'Ubuntu' and V(distrib_release()) >= V('14.04'))
        at_least_jessie = (
            distrib == 'Debian' and V(distrib_release()) >= V('8.0'))
        if at_least_trusty or at_least_jessie:
            return new_style
        else:
            return old_style
    else:
        raise UnsupportedFamily(supported=['debian'])


# backward compatibility (deprecated)
enable = enable_site
disable = disable_site

__all__ = [
    'is_module_enabled', 'enable_module', 'disable_module',
    'is_site_enabled', 'enable_site', 'disable_site',
]
