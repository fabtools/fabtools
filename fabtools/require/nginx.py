"""
Idempotent API for managing nginx sites
"""
from fabric.api import *
from fabtools.files import upload_template, is_link
from fabtools.require.deb import package
from fabtools.require.service import started


def server():
    """
    Require an nginx server
    """
    package('nginx')
    started('nginx')


def site(server_name, options=None, enabled=True):
    """
    Require an nginx site
    """
    if options is None:
        options = {}
    options['server_name'] = server_name

    upload_template('/etc/nginx/sites-available/%(server_name)s.conf' % locals(),
        'nginx/sites/%(server_name)s.conf' % locals(),
        context=options,
        use_sudo=True)

    if enabled:
        if not is_link('/etc/nginx/sites-enabled/%(server_name)s.conf' % locals()):
            sudo("ln -s /etc/nginx/sites-available/%(server_name)s.conf /etc/nginx/sites-enabled/%(server_name)s.conf" % locals())
    else:
        if is_link('/etc/nginx/sites-enabled/%(server_name)s.conf' % locals()):
            sudo("rm /etc/nginx/sites-enabled/%(server_name)s.conf" % locals())

    sudo("/etc/init.d/nginx reload")
