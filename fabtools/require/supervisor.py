"""
Idempotent API for managing supervisor processes
"""
from fabtools.require import deb
from fabtools.require.files import template_file
from fabtools.supervisor import *


DEFAULT_TEMPLATE = """\
[program:%(name)s]
command=%(command)s
directory=%(directory)s
user=%(user)s
autostart=true
autorestart=true
redirect_stderr=true
"""


def process(name, template_contents=None, template_source=None, **kwargs):
    """
    Require a supervisor process
    """
    deb.package('supervisor')

    config_filename = '/etc/supervisor/conf.d/%s.conf' % name

    context = {}
    context.update(kwargs)
    context['name'] = name

    if (template_contents is None) and (template_source is None):
        template_contents = DEFAULT_TEMPLATE

    template_file(config_filename, template_contents, template_source, context, use_sudo=True)

    reload_config()

    if process_status(name) == 'STOPPED':
        start_process(name)
