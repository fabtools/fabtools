"""
Idempotent API for managing supervisor processes
"""
from __future__ import with_statement

from fabtools.files import watch
from fabtools.supervisor import *


def process(name, **kwargs):
    """
    Require a supervisor process
    """
    from fabtools import require

    require.deb.package('supervisor')
    require.service.started('supervisor')

    # Set default parameters
    params = {}
    params.update(kwargs)
    params.setdefault('autorestart', 'true')
    params.setdefault('redirect_stderr', 'true')

    # Build config file from parameters
    lines = []
    lines.append('[program:%(name)s]' % locals())
    for key, value in sorted(params.items()):
        lines.append("%s=%s" % (key, value))

    # Upload config file
    filename = '/etc/supervisor/conf.d/%(name)s.conf' % locals()
    with watch(filename, True, reload_config):
        require.file(filename, contents='\n'.join(lines), use_sudo=True)

    # Start the process if needed
    if process_status(name) == 'STOPPED':
        start_process(name)
