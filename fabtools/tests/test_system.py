from mock import patch

import pytest


def test_unsupported_system():

    from fabtools.system import UnsupportedFamily

    with pytest.raises(UnsupportedFamily) as excinfo:

        with patch('fabtools.system.distrib_id') as mock_distrib_id:
            mock_distrib_id.return_value = 'foo'

            raise UnsupportedFamily(supported=['debian', 'redhat'])

    exception_msg = str(excinfo.value)
    assert exception_msg == "Unsupported family other (foo). Supported families: debian, redhat"
