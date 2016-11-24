import pytest


pytestmark = pytest.mark.network


@pytest.fixture(scope='module')
def firewall():
    from fabtools.require.shorewall import firewall
    import fabtools.shorewall
    firewall(
        rules=[
            fabtools.shorewall.Ping(),
            fabtools.shorewall.SSH(),
            fabtools.shorewall.HTTP(),
            fabtools.shorewall.HTTPS(),
            fabtools.shorewall.SMTP(),
            fabtools.shorewall.rule(
                port=1234,
                source=fabtools.shorewall.hosts(['example.com']),
            ),
        ]
    )


def test_require_firewall_started(firewall):
    from fabtools.require.shorewall import started
    from fabtools.shorewall import is_started
    started()
    assert is_started()


def test_require_firewall_stopped(firewall):
    from fabtools.require.shorewall import stopped
    from fabtools.shorewall import is_stopped
    stopped()
    assert is_stopped()
