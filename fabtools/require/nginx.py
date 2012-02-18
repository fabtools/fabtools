"""
Idempotent API for managing nginx sites
"""
from __future__ import with_statement

from fabric.api import *
from fabric.colors import red
from fabtools.files import upload_template, is_link
from fabtools.require.deb import package
from fabtools.require.files import template_file
from fabtools.require.service import started


def server():
    """
    Require an nginx server
    """
    package('nginx')
    started('nginx')


def site(server_name, template_contents=None, template_source=None, enabled=True, check_config=True, **kwargs):
    """
    Require an nginx site
    """
    server()

    config_filename = '/etc/nginx/sites-available/%s.conf' % server_name

    context = {
        'port': 80,
    }
    context.update(kwargs)
    context['server_name'] = server_name

    template_file(config_filename, template_contents, template_source, context, use_sudo=True)

    link_filename = '/etc/nginx/sites-enabled/%s.conf' % server_name
    if enabled:
        if not is_link(link_filename):
            sudo("ln -s %(config_filename)s %(link_filename)s" % locals())

        # Make sure we don't break the config
        if check_config:
            with settings(hide('running', 'warnings'), warn_only=True):
                if sudo("nginx -t").return_code > 0:
                    print red("Error in %(server_name)s nginx site config (disabling for safety)" % locals())
                    sudo("rm %(link_filename)s" % locals())
    else:
        if is_link(link_filename):
            sudo("rm %(link_filename)s" % locals())

    sudo("/etc/init.d/nginx reload")


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
    Require an nginx site for a proxied app
    """
    site(server_name, template_contents=PROXIED_SITE_TEMPLATE, enabled=enabled, **kwargs)
