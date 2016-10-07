"""
Nginx
=====

This module provides high-level tools for installing the `nginx`_
web server and managing the configuration of web sites.

.. _nginx: http://nginx.org/

"""

from fabric.api import (
    abort,
    hide,
    settings,
)
from fabric.colors import red

from fabtools.deb import is_installed
from fabtools.files import is_link
from fabtools.nginx import disable, enable
from fabtools.service import reload as reload_service
from fabtools.system import UnsupportedFamily, distrib_family
from fabtools.utils import run_as_root

from fabtools.require.files import template_file
from fabtools.require.service import started as require_started


def server(package_name='nginx'):
    """
    Require the nginx web server to be installed and running.

    You can override the system package name, if you need to install
    a specific variant such as `nginx-extras` or `nginx-light`.

    ::

        from fabtools import require

        require.nginx.server()

    """
    family = distrib_family()
    if family == 'debian':
        _server_debian(package_name)
    else:
        raise UnsupportedFamily(supported=['debian'])


def _server_debian(package_name):

    from fabtools.require.deb import package as require_deb_package

    require_deb_package(package_name)
    require_started('nginx')


def enabled(config):
    """
    Require an nginx site to be enabled.

    This will cause nginx to reload its configuration.

    ::

        from fabtools import require

        require.nginx.enabled('mysite')

    """
    enable(config)
    reload_service('nginx')


def disabled(config):
    """
    Require an nginx site to be disabled.

    This will cause nginx to reload its configuration.

    ::

        from fabtools import require

        require.nginx.disabled('default')

    """
    disable(config)
    reload_service('nginx')


def site(server_name, template_contents=None, template_source=None,
         enabled=True, check_config=True, **kwargs):
    """
    Require an nginx site.

    You must provide a template for the site configuration, either as a
    string (*template_contents*) or as the path to a local template
    file (*template_source*).

    ::

        from fabtools import require

        CONFIG_TPL = '''
        server {
            listen      %(port)d;
            server_name %(server_name)s %(server_alias)s;
            root        %(docroot)s;
            access_log  /var/log/nginx/%(server_name)s.log;
        }'''

        require.nginx.site('example.com',
            template_contents=CONFIG_TPL,
            port=80,
            server_alias='www.example.com',
            docroot='/var/www/mysite',
        )

    .. seealso:: :py:func:`fabtools.require.files.template_file`
    """
    if not is_installed('nginx-common'):
        # nginx-common is always installed if nginx exists
        server()

    config_filename = '/etc/nginx/sites-available/%s.conf' % server_name

    context = {
        'port': 80,
    }
    context.update(kwargs)
    context['server_name'] = server_name

    template_file(config_filename, template_contents, template_source,
                  context, use_sudo=True)

    link_filename = '/etc/nginx/sites-enabled/%s.conf' % server_name
    if enabled:
        if not is_link(link_filename):
            run_as_root(
                "ln -s %(config_filename)s %(link_filename)s" % locals())

        # Make sure we don't break the config
        if check_config:
            with settings(hide('running', 'warnings'), warn_only=True):
                if run_as_root('nginx -t').failed:
                    run_as_root("rm %(link_filename)s" % locals())
                    message = red("Error in %(server_name)s nginx site config (disabling for safety)" % locals())
                    abort(message)
    else:
        if is_link(link_filename):
            run_as_root("rm %(link_filename)s" % locals())

    reload_service('nginx')


PROXIED_SITE_TEMPLATE = """\
server {
    listen %(port)s;
    server_name %(server_name)s;

    gzip_vary on;

    # path for static files
    root %(docroot)s;

    try_files $uri @proxied;

    location @proxied {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass %(proxy_url)s;
    }

    access_log /var/log/nginx/%(server_name)s.log;
}
"""


def proxied_site(server_name, enabled=True, **kwargs):
    """
    Require an nginx site for a proxied app.

    This uses a predefined configuration template suitable for proxying
    requests to a backend application server.

    Required keyword arguments are:

    - *port*: the port nginx should listen on
    - *proxy_url*: URL of backend application server
    - *docroot*: path to static files

    ::

        from fabtools import require

        require.nginx.proxied_site('example.com',
            port=80,
            proxy_url='http://127.0.0.1:8080/',
            docroot='/path/to/myapp/static',
        )
    """
    site(server_name, template_contents=PROXIED_SITE_TEMPLATE,
         enabled=enabled, **kwargs)
