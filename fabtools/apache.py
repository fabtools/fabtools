"""
Apache
======

This module provides tools for configuring
the `Apache HTTP Server <http://httpd.apache.org/>`_.

"""
from fabtools.files import is_link
from fabtools.utils import run_as_root


def _get_link_filename(config):
    return '/etc/apache2/sites-enabled/%s' % config


def _get_config_name(config):
    if config not in ('default', 'default-ssl'):
        config += '.conf'

    return config


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


def is_site_enabled(config):
    """
    Check if an Apache site is enabled.
    """
    config = _get_config_name(config)
    if config == 'default':
        config = '000-default'

    return is_link(_get_link_filename(config))


def enable_site(config):
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
    if not is_site_enabled(config):
        run_as_root('a2ensite %s' % _get_config_name(config))


def disable_site(config):
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
    if is_site_enabled(config):
        run_as_root('a2dissite %s' % _get_config_name(config))


# backward compatibility (deprecated)
enable = enable_site
disable = disable_site

__all__ = [
    'is_module_enabled', 'enable_module', 'disable_module',
    'is_site_enabled', 'enable_site', 'disable_site',
]
