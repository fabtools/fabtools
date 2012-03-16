from fabric.api import *
from fabtools import require
import fabtools


@task
def firewall():
    """
    Setup a firewall
    """
    require.shorewall.firewall(
        rules=[
            fabtools.shorewall.Ping(),
            fabtools.shorewall.SSH(),
            fabtools.shorewall.HTTP(),
            fabtools.shorewall.HTTPS(),
            fabtools.shorewall.SMTP(),
            fabtools.shorewall.rule(port=1234,
                source=fabtools.shorewall.hosts(['example.com'])),
        ]
    )

    require.shorewall.started()
    assert fabtools.shorewall.is_started()

    require.shorewall.stopped()
    assert fabtools.shorewall.is_stopped()
