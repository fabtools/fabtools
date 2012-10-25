from __future__ import with_statement

from fabric.api import *
from fabtools import require


@task
def locales():
    """
    Check locales configuration
    """
    require.system.locale('en_US.UTF-8')
    require.system.locale('fr_FR.UTF-8')
