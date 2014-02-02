from fabtools.tests.vagrant_test_case import VagrantTestCase


class TestLocales(VagrantTestCase):

    def test_en_locale(self):
        from fabtools.require.system import locale
        locale('en_US.UTF-8')

    def test_fr_locale(self):
        from fabtools.require.system import locale
        locale('fr_FR.UTF-8')
