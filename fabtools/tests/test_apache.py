from mock import patch
import pytest


@pytest.yield_fixture
def debian_family():
    with patch('fabtools.apache.distrib_family') as mock:
        mock.return_value = 'debian'
        yield


@pytest.yield_fixture
def debian(debian_family):
    with patch('fabtools.apache.distrib_id') as mock:
        mock.return_value = 'Debian'
        yield


@pytest.yield_fixture
def debian_8_0(debian):
    with patch('fabtools.apache.distrib_release') as mock:
        mock.return_value = '8.0'
        yield


@pytest.yield_fixture
def debian_7_2(debian):
    with patch('fabtools.apache.distrib_release') as mock:
        mock.return_value = '7.2'
        yield


@pytest.yield_fixture
def ubuntu(debian_family):
    with patch('fabtools.apache.distrib_id') as mock:
        mock.return_value = 'Ubuntu'
        yield


@pytest.yield_fixture
def ubuntu_12_04(ubuntu):
    with patch('fabtools.apache.distrib_release') as mock:
        mock.return_value = '12.04'
        yield


@pytest.yield_fixture
def ubuntu_14_04(ubuntu):
    with patch('fabtools.apache.distrib_release') as mock:
        mock.return_value = '14.04'
        yield


def test_default_site_filename_debian_7_2(debian_7_2):
    from fabtools.apache import _site_config_filename
    assert _site_config_filename('default') == 'default'


def test_default_site_linkname_debian_7_2(debian_7_2):
    from fabtools.apache import _site_link_filename
    assert _site_link_filename('default') == '000-default'


def test_default_site_filename_debian_8_0(debian_8_0):
    from fabtools.apache import _site_config_filename
    assert _site_config_filename('default') == '000-default.conf'


def test_default_site_linkname_debian_8_0(debian_8_0):
    from fabtools.apache import _site_link_filename
    assert _site_link_filename('default') == '000-default.conf'


def test_default_site_filename_ubuntu_12_04(ubuntu_12_04):
    from fabtools.apache import _site_config_filename
    assert _site_config_filename('default') == 'default'


def test_default_site_linkname_ubuntu_12_04(ubuntu_12_04):
    from fabtools.apache import _site_link_filename
    assert _site_link_filename('default') == '000-default'


def test_default_site_filename_ubuntu_14_04(ubuntu_14_04):
    from fabtools.apache import _site_config_filename
    assert _site_config_filename('default') == '000-default.conf'


def test_default_site_linkname_ubuntu_14_04(ubuntu_14_04):
    from fabtools.apache import _site_link_filename
    assert _site_link_filename('default') == '000-default.conf'


def test__site_config_filename():
    from fabtools.apache import _site_config_filename
    assert _site_config_filename('foo') == 'foo.conf'
