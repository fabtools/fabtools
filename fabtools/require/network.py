"""
Network packages
==================

"""
from __future__ import with_statement

import re

from fabric.api import hide
from fabric.contrib.files import sed, append

from fabtools.utils import run_as_root


def host(ipaddress, hostnames, use_sudo=False):
    """
    Add a ipadress and hostname(s) in /etc/hosts file

    Example::
        from fabtools import require

        require.network.host('127.0.0.1','hostname-a hostname-b')
    """

    res = run_as_root('cat /etc/hosts | egrep "^%(ipaddress)s"' % locals())
    if res.succeeded:
        m = re.match('^%(ipaddress)s (.*)' % locals(), res)

        # If ipadress allready exists
        if m:
            toadd = list()
            hostnames = hostnames.split(' ')
            inthehosts = m.group(1).split(' ')
            for h in hostnames:
                if h not in inthehosts:
                    toadd.append(h)

            if len(toadd) > 0:
                print "ADD: %s" % toadd
                print res
                hostline = "%s %s" % (res, ' '.join(toadd))

                with hide('stdout', 'warnings'):
                    sed('/etc/hosts', res, hostline, use_sudo=use_sudo)
        else:
            hostline = "%s %s" % (res, hostnames)
            append('/etc/hosts', hostline, use_sudo=use_sudo)
