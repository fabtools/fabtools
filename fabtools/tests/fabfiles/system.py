from __future__ import with_statement

from fabric.api import task


@task
def locales():
    """
    Check locales configuration
    """

    from fabtools import require

    require.system.locale('en_US.UTF-8')
    require.system.locale('fr_FR.UTF-8')
