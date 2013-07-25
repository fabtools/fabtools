"""
Apache
======

This module provides high-level tools for installing the `apache2 <http://httpd.apache.org/>`_
web server and managing the configuration of web sites.

"""
from __future__ import with_statement

from fabric.api import (
    abort,
    hide,
    settings,
)
from fabric.colors import red

from fabtools.apache import disable, enable, _get_config_name
from fabtools.require.deb import package
from fabtools.require.files import template_file
from fabtools.require.service import started as require_started
from fabtools.service import reload as reload_service
from fabtools.utils import run_as_root


def server():
    """
    Require apache2 server to be installed and running.

    ::

        from fabtools import require

        require.apache.server()
    """
    package('apache2')
    require_started('apache2')


def enabled(config):
    """
    Ensure link to /etc/apache2/sites-available/config exists and reload apache2
    configuration if needed.
    """
    enable(config)
    reload_service('apache2')


def disabled(config):
    """
    Ensure link to /etc/apache2/sites-available/config doesn't exist and reload
    apache2 configuration if needed.
    """
    disable(config)
    reload_service('apache2')


def site(config_name, template_contents=None, template_source=None, enabled=True, check_config=True, **kwargs):
    """
    Require an apache2 site.

    You must provide a template for the site configuration, either as a
    string (*template_contents*) or as the path to a local template
    file (*template_source*).

    ::

        from fabtools import require

        CONFIG_TPL = '''
        <VirtualHost *:%(port)s>
            ServerName %(hostname})s

            DocumentRoot %(document_root)s

            <Directory %(document_root)s>
                Options Indexes FollowSymLinks MultiViews

                AllowOverride All

                Order allow,deny
                allow from all
            </Directory>
        </VirtualHost>
        '''

        require.apache.site(
            'example.com',
            template_contents=CONFIG_TPL,
            port=80,
            hostname='www.example.com',
            document_root='/var/www/mysite',
        )

    .. seealso:: :py:func:`fabtools.require.files.template_file`
    """
    server()

    config_filename = '/etc/apache2/sites-available/%s' % _get_config_name(config_name)

    context = {
        'port': 80,
    }
    context.update(kwargs)
    context['config_name'] = config_name

    template_file(config_filename, template_contents, template_source, context, use_sudo=True)

    if enabled:
        enable(config_name)
    else:
        disable(config_name)

    if check_config:
        with settings(hide('running', 'warnings'), warn_only=True):
            if run_as_root('apache2ctl configtest').failed:
                disable(config_name)
                message = red("Error in %(config_name)s apache site config (disabling for safety)" % locals())
                abort(message)

    reload_service('apache2')
