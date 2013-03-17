from __future__ import with_statement

from fabric.api import task


@task
def md5():
    """
    Check MD5 sums (unavailable, empty, with content)
    """

    import hashlib

    from fabric.api import cd, hide, run, settings
    import fabtools

    with cd('/tmp'):

        run('touch f1')
        assert fabtools.files.md5sum('f1') == hashlib.md5('').hexdigest()

        run('echo -n hello > f2')
        assert fabtools.files.md5sum('f2') == hashlib.md5('hello').hexdigest()

        with settings(hide('warnings')):
            assert fabtools.files.md5sum('doesnotexist') is None
