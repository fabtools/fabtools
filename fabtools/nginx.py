"""
Nginx
=====

This module provides tools for managing Nginx config files.

"""
from pipes import quote

from fabric.api import *
from fabtools.files import is_link


def enable(config):
    """
    Create link from /etc/nginx/sites-available/ in /etc/nginx/sites-enabled/

    (does not reload nginx config)

    ::
        from fabtools import require

        require.nginx.enable('default')

    .. seealso:: :py:func:`fabtools.require.nginx.enabled`
    """
    config_filename = '/etc/nginx/sites-available/%s' % config
    link_filename = '/etc/nginx/sites-enabled/%s' % config

    if not is_link(link_filename):
        sudo("ln -s %(config_filename)s %(link_filename)s" % {
                'config_filename': quote(config_filename),
                'link_filename': quote(link_filename),
        })


def disable(config):
    """
    Delete link in /etc/nginx/sites-enabled/

    (does not reload nginx config)

    ::
        from fabtools import require

        require.nginx.disable('default')

    .. seealso:: :py:func:`fabtools.require.nginx.disabled`
    """
    link_filename = '/etc/nginx/sites-enabled/%s' % config

    if is_link(link_filename):
        sudo("rm %(link_filename)s" % locals())
