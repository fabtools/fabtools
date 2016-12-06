from fabric.api import puts, sudo

from fabtools.require.files import directory as require_directory


def test_list_partitions():
    """
    List disk partitions
    """

    from fabtools.disk import partitions

    partitions = partitions()
    for pname, ptype in partitions.items():
        puts("%s is %s" % (pname, hex(ptype)))


def test_format_and_mount():
    """
    Format, mount and unmount a block device
    """

    from fabtools.disk import ismounted, mkfs, mount

    assert not ismounted('/dev/loop0')

    try:
        # Make a loopback block device
        sudo('dd if=/dev/zero of=bigfile bs=1024 count=30720')
        sudo('losetup /dev/loop0 bigfile')

        # Format the block device
        mkfs('/dev/loop0', 'ext3')

        # Mount the block device
        require_directory('/mnt/loop', use_sudo=True)
        mount('/dev/loop0', '/mnt/loop')
        assert ismounted('/dev/loop0')

        # Unmount the block device
        sudo('umount /dev/loop0')
        assert not ismounted('/dev/loop0')

    finally:
        sudo('umount /dev/loop0', quiet=True)
        sudo('losetup -d /dev/loop0', quiet=True)
        sudo('rm -f bigfile', quiet=True)
