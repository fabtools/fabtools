from fabtools.files import is_link
from fabtools.utils import run_as_root


def _get_link_filename(config):
    return '/etc/apache2/sites-enabled/%s' % config


def _get_config_name(config):
    if config not in ('default', 'default-ssl'):
        config += '.conf'

    return config


def is_site_enabled(config):
    config = _get_config_name(config)
    if config == 'default':
        config = '000-default'

    return is_link(_get_link_filename(config))


def enable(config):
    """
    Create link from /etc/apache2/sites-available/ in /etc/apache2/sites-enabled/

    (does not reload apache config)

    ::

        from fabtools import require

        require.apache.enable('default')

    .. seealso:: :py:func:`fabtools.require.apache.enabled`
    """
    if not is_site_enabled(config):
        run_as_root('a2ensite %s' % _get_config_name(config))


def disable(config):
    """
    Delete link in /etc/apache/sites-enabled/

    (does not reload apache config)

    ::

        from fabtools import require

        require.apache.disable('default')

    .. seealso:: :py:func:`fabtools.require.apache.disabled`
    """
    if is_site_enabled(config):
        run_as_root('a2dissite %s' % _get_config_name(config))
