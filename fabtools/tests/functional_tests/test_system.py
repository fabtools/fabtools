import pytest


class TestRequireLocale:

    def test_en_locale(self):
        from fabtools.require.system import locale
        locale('en_US')

    def test_fr_locale(self):
        from fabtools.require.system import locale
        locale('fr_FR')

    def test_non_existing_locale(self):
        from fabtools.require.system import locale, UnsupportedLocales
        with pytest.raises(UnsupportedLocales) as excinfo:
            locale('ZZZZ')
        assert excinfo.value.locales == ['ZZZZ']
