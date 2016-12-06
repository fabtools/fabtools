"""
Disk Tools
==========
"""

import re

from fabric.api import hide, settings, abort

from fabtools.utils import run_as_root


def partitions(device=""):
    """
    Get a partition list for all disk or for selected device only

    Example::

        from fabtools.disk import partitions

        spart = {'Linux': 0x83, 'Swap': 0x82}
        parts = partitions()
        # parts =  {'/dev/sda1': 131, '/dev/sda2': 130, '/dev/sda3': 131}
        r = parts['/dev/sda1'] == spart['Linux']
        r = r and parts['/dev/sda2'] == spart['Swap']
        if r:
            print("You can format these partitions")
    """
    partitions_list = {}
    with settings(hide('running', 'stdout')):
        res = run_as_root('sfdisk -d %(device)s' % locals())

        # Old SFIDSK
        spartid = re.compile(r'(?P<pname>^/.*) : .* Id=(?P<ptypeid>[0-9a-z]+)')
        # New SFDISK
        sparttype = re.compile(r'(?P<pname>^/.*) : .* type=(?P<ptypeid>[0-9a-z]+)')
        for line in res.splitlines():

            # Old SFIDSK
            m = spartid.search(line)
            if m:
                partitions_list[m.group('pname')] = int(m.group('ptypeid'), 16)
            else:
                # New SFDISK
                m = sparttype.search(line)
                if m:
                    partitions_list[m.group('pname')] = int(m.group('ptypeid'), 16)

    return partitions_list


def getdevice_by_uuid(uuid):
    """
    Get a HDD device by uuid

    Example::

        from fabtools.disk import getdevice_by_uuid

        device = getdevice_by_uuid("356fafdc-21d5-408e-a3e9-2b3f32cb2a8c")
        if device:
            mount(device,'/mountpoint')
    """
    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        res = run_as_root('blkid -U %s' % uuid)

        if not res.succeeded:
            return None

        return res


def mount(device, mountpoint):
    """
    Mount a partition

    Example::

        from fabtools.disk import mount

        mount('/dev/sdb1', '/mnt/usb_drive')
    """
    if not ismounted(device):
        run_as_root('mount %(device)s %(mountpoint)s' % locals())


def swapon(device):
    """
    Active swap partition

    Example::

        from fabtools.disk import swapon

        swapon('/dev/sda1')
    """
    if not ismounted(device):
        run_as_root('swapon %(device)s' % locals())


def ismounted(device):
    """
    Check if partition is mounted

    Example::

        from fabtools.disk import ismounted

        if ismounted('/dev/sda1'):
           print ("disk sda1 is mounted")
    """
    # Check filesystem
    with settings(hide('running', 'stdout')):
        res = run_as_root('mount')
    for line in res.splitlines():
        fields = line.split()
        if fields[0] == device:
            return True

    # Check swap
    with settings(hide('running', 'stdout')):
        res = run_as_root('swapon -s')
    for line in res.splitlines():
        fields = line.split()
        if fields[0] == device:
            return True

    return False


def mkfs(device, ftype):
    """
    Format filesystem

    Example::

        from fabtools.disk import mkfs

        mkfs('/dev/sda2', 'ext4')
    """
    if not ismounted('%(device)s' % locals()):
        run_as_root('mkfs.%(ftype)s %(device)s' % locals())
    else:
        abort("Partition is mounted")


def mkswap(device):
    """
    Format swap partition

    Example::

        from fabtools.disk import mkswap

        mkswap('/dev/sda2')
    """
    if not ismounted(device):
        run_as_root('mkswap %(device)s' % locals())
    else:
        abort("swap partition is mounted")
