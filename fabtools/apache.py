from fabtools.files import is_link
from fabtools.utils import run_as_root


def _get_link_filename(config):
    return '/etc/apache2/sites-enabled/%s' % config


def _get_config_name(config):
    if config not in ('default', 'default-ssl'):
        config += '.conf'

    return config


def is_module_enabled(module):
    return is_link('/etc/apache2/mods-enabled/%s.load' % module)


def enable_module(module):
    """
    Create link from /etc/apache2/mods-available/ in /etc/apache2/mods-enabled/

    (does not reload apache config)

    ::

        from fabtools import require

        require.apache.enable_module('rewrite')

    .. seealso:: :py:func:`fabtools.require.apache.module_enabled`
    """
    if not is_module_enabled(module):
        run_as_root('a2enmod %s' % module)


def disable_module(module):
    """
    Delete link in /etc/apache/mods-enabled/

    (does not reload apache config)

    ::

        from fabtools import require

        require.apache.disable_module('rewrite')

    .. seealso:: :py:func:`fabtools.require.apache.module_disabled`
    """
    if is_module_enabled(module):
        run_as_root('a2dismod %s' % module)


def is_site_enabled(config):
    config = _get_config_name(config)
    if config == 'default':
        config = '000-default'

    return is_link(_get_link_filename(config))


def enable_site(config):
    """
    Create link from /etc/apache2/sites-available/ in /etc/apache2/sites-enabled/

    (does not reload apache config)

    ::

        from fabtools import require

        require.apache.enable_site('default')

    .. seealso:: :py:func:`fabtools.require.apache.site_enabled`
    """
    if not is_site_enabled(config):
        run_as_root('a2ensite %s' % _get_config_name(config))


def disable_site(config):
    """
    Delete link in /etc/apache/sites-enabled/

    (does not reload apache config)

    ::

        from fabtools import require

        require.apache.disable_site('default')

    .. seealso:: :py:func:`fabtools.require.apache.site_disabled`
    """
    if is_site_enabled(config):
        run_as_root('a2dissite %s' % _get_config_name(config))


# backward compatibility (deprecated)
enable = enable_site
disable = disable_site
