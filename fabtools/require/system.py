"""
System settings
===============
"""

from re import escape

from fabric.api import settings
from fabric.contrib.files import append, uncomment

from fabtools.files import is_file, watch
from fabtools.system import (
    UnsupportedFamily,
    distrib_family, distrib_id,
    get_hostname, set_hostname,
    get_sysctl, set_sysctl,
    supported_locales,
)
from fabtools.utils import run_as_root


class UnsupportedLocales(Exception):

    def __init__(self, locales):
        self.locales = sorted(locales)
        msg = "Unsupported locales: %s" % ', '.join(self.locales)
        super(UnsupportedLocales, self).__init__(msg)


def sysctl(key, value, persist=True):
    """
    Require a kernel parameter to have a specific value.
    """
    if get_sysctl(key) != value:
        set_sysctl(key, value)

    if persist:

        from fabtools.require import file as require_file

        filename = '/etc/sysctl.d/60-%s.conf' % key
        with watch(filename, use_sudo=True) as config:
            require_file(filename,
                         contents='%(key)s = %(value)s\n' % locals(),
                         use_sudo=True)
        if config.changed:
            if distrib_family() == 'debian':
                with settings(warn_only=True):
                    run_as_root('service procps start')


def hostname(name):
    """
    Require the hostname to have a specific value.
    """
    if get_hostname() != name:
        set_hostname(name)


def locales(names):
    """
    Require the list of locales to be available.

    Raises UnsupportedLocales if some of the required locales
    are not supported.
    """

    family = distrib_family()
    if family == 'debian':
        command = 'dpkg-reconfigure --frontend=noninteractive locales'
        if distrib_id() == 'Ubuntu':
            config_file = '/var/lib/locales/supported.d/local'
            if not is_file(config_file):
                run_as_root('touch %s' % config_file)
        else:
            config_file = '/etc/locale.gen'
        _locales_generic(names, config_file=config_file, command=command)
    elif family in ['arch', 'gentoo']:
        _locales_generic(names, config_file='/etc/locale.gen',
                         command='locale-gen')
    elif distrib_family() == 'redhat':
        _locales_redhat(names)
    else:
        raise UnsupportedFamily(
            supported=['debian', 'arch', 'gentoo', 'redhat'])


def _locales_generic(names, config_file, command):

    supported = supported_locales()
    _check_for_unsupported_locales(names, supported)

    # Regenerate locales if config file changes
    with watch(config_file, use_sudo=True) as config:

        # Add valid locale names to the config file
        charset_from_name = dict(supported)
        for name in names:
            charset = charset_from_name[name]
            locale = "%s %s" % (name, charset)
            uncomment(config_file, escape(locale), use_sudo=True, shell=True)
            append(config_file, locale, use_sudo=True,
                   partial=True, shell=True)

    if config.changed:
        run_as_root(command)


def _locales_redhat(names):
    supported = supported_locales()
    _check_for_unsupported_locales(names, supported)


def _check_for_unsupported_locales(names, supported):
    missing = set(names) - set([name for name, _ in supported])
    if missing:
        raise UnsupportedLocales(missing)


def locale(name):
    """
    Require the locale to be available.

    Raises UnsupportedLocales if the required locale is not supported.
    """
    locales([name])


def default_locale(name):
    """
    Require the locale to be the default.
    """
    from fabtools.require import file as require_file

    # Ensure the locale is available
    locale(name)

    # Make it the default
    contents = 'LANG="%s"\n' % name
    if distrib_family() == 'arch':
        config_file = '/etc/locale.conf'
    else:
        config_file = '/etc/default/locale'
    require_file(config_file, contents, use_sudo=True)
