import hashlib

from fabric.api import hide, run, settings

import fabtools


def test_md5sum_empty_file():
    try:
        run('touch f1')
        expected_hash = hashlib.md5('').hexdigest()
        assert fabtools.files.md5sum('f1') == expected_hash
    finally:
        run('rm -f f1')


def test_md5sum():
    try:
        run('echo -n hello > f2')
        expected_hash = hashlib.md5('hello').hexdigest()
        assert fabtools.files.md5sum('f2') == expected_hash
    finally:
        run('rm -f f2')


def test_md5sum_not_existing_file():
    with settings(hide('warnings')):
        assert fabtools.files.md5sum('doesnotexist') is None
