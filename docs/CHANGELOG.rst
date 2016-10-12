Changelog
=========

0.20.0 (2016-10-12)
-------------------

* Fix Apache support on Ubuntu 14.04 and Debian 8.0
* Change maxsplit argument value to 1 for vagrant
* Fix nodejs fails to read json
* Fix typo in PostgreSQL require documentation
* Fix typo in files and nginx documentation
* Clean the code and be pep8 compliant
* In PostgreSQL put the username in double quotes
* Use Python 3 compatible print statement when checking setuptools
* In network add MAC address information
* Add support for conda package manager
* Add the support of host options for MySQL
* Fix different sfdisk version


Version 0.19.0 (2014-07-05)
---------------------------

* Python improvements:
    * use new official download URLs for ``setuptools`` and ``pip`` (Arnaud Vazard)
    * fix ``virtualenv`` when the ``local`` flag is passed (Troy J. Farrell)
* Node.js improvements:
    * fix ``package_version`` when no package is installed (Alexandre Patry)
    * add a ``checkinstall`` flasg to build and install a distribution package
      when installing from source (Fabien Meghazi)
* Arch Linux improvements:
    * add support for the ManjaroLinux variant (Gaëtan Lamothe)
    * fixsupport for ``setuptools`` (Robin Lambertz)
    * fix support for ``supervisor`` (Robin Lambertz)
    * recognize all known distribution IDs and normalize them to ``Arch``
* Debian/Ubuntu improvements:
    * add support for the Elementary OS variant (Arnaud Vazard)


Version 0.18.0 (2014-05-02)
---------------------------

This release requires Fabric >= 1.7.0 and drops support for Python 2.5.

* Add ``drop_user`` and ``drop_database`` in ``postgres`` module
* Add LinuxMint to the Debian family list (Frank Rousseau)
* Add support for git remotes (Bryan Folliot)
* Add support for Tomcat (Jan Kowalski)
* Add support for Gentoo / portage (Travis Shirk)
* Add support for Mercurial (Travis Shirk)
* Add support for GVM (Groovy environment manager) (Bryan Folliot)
* Documentation fixes and updates
* MySQL improvements:
    * do not require a password when a specific user is specified
    * expose ``mysql.query`` in the public API
* Python improvements:
    * Switch to pip 1.5 (**warning**: you will need to use the
      ``allow_external`` and/or ``allow_unverified`` options to install
      packages not hosted on PyPI)
    * Update GitHub download URL for pip installer (Guillaume Andreu Sabater)
    * Retry when trying to download pip/setuptools installers
    * Add support for pip's ``--exists-action`` option
* Improved OS support in ``distrib_family()`` and new
  ``UnsupportedFamily`` exception
* Make sure to install ``curl`` before using it (ponty)
* Vagrant improvements:
    * Add function to get the Vagrant version
    * Add function to get the status of a Vagrant machine
    * Add function to get the list of Vagrant machines
    * Add function to get the list of Vagrant base boxes
* Files improvements:
    * Add ``temp_dir`` parameter to ``require.file`` (default is ``tmp``)
    * Add ``require.files.temporary_directory``
    * Add ``files.umask`` to get the user's umask
    * Fix ``require.file`` ownership and permissions when using ``sudo``
    * Add helpers to copy, move, symlink or remove files
* Fix ``require.deb.uptodate_index``
* Use ``rpm`` instead of ``yum`` to check if an RPM package is installed
* Update JDK install to match changes to the Oracle web site
* Fix ``cron.add_task`` (thanks to Dan Fairs and Ikuya Yamada)


Version 0.17.0 (2013-12-06)
---------------------------

* Vagrant improvements:
    * Fix support for Vagrant >= 1.3.0
    * Fix duplicate function in ``vagrant`` module documentation
      (Dean Malmgren)
* Package management improvements:
    * Ubuntu PPA fixes (Anthony Scalisi)
    * Add support for ``opkg`` package manager (ponty)
    * Add conditional APT index updates, based on the time of the
      last update (ponty)
* Update ``files.upload_template`` to match Fabric parameters
  (thanks to Adam Patterson)
* PostgreSQL improvements:
    * Fix: use ``run`` instead of ``sudo`` in ``_run_as_pg`` (iiie)
    * Improve SmartOS and locale support (Andreas Kaiser)
* Support tags in addition to branches in
  ``require.git.working_copy`` (Andreas Kaiser)
* Services management improvements:
    * Improve upstart support in ``service.is_running`` (John MacKenzie)
    * Add support for ``systemd`` in ``service.is_running``
      (Adrien Raffin)
* Improve support for Arch Linux in ``nodejs``, ``service`` and
  ``supervisor`` modules (Steeve Chailloux)
* Allow custom ``nginx`` package names (Laurent Meunier)
* Add module management for Apache (Eugene Leonovich)
* Fix test environment for Python 2.5
* Use the new Read the Docs theme if available when
  building the docs locally
* Fix bug with user/group creation with int UID/GID


Version 0.16.0 (2013-10-26)
---------------------------

* Redis improvements
    * Make bind and port arguments explicit
    * Improve documentation
    * Upgrade default version to 2.6.16
* Python improvements
    * Improve support for using specific Python interpreters (**warning**:
      API changes)
    * Expose low-level virtualenv operations
    * Improve pip installation
    * Switch from distribute to setuptools 0.7+ after project merge
      (**warning**: API changes)
    * Do not install `curl` and `python-dev` packages when setuptools
      is already installed (ponty)
    * Make package names case-insensitive in python.is_installed
      (ponty)
    * Fix pip version parsing when using ``pythonbrew switch``
* Fix ``require.system.locales`` when a prefix is set
* Fix require.system.locale() on fresh Ubuntu systems
* Add optional environment variables in crontab
* Fix crontab permissions
* Allow special characters in MySQL password (Régis Behmo)
* Fix bug with some services not starting correctly (Chris Marinos)
* Add ``getdevice_by_uuid`` to the disk module (Bruno Adele)
* Fix implicit directory name in ``git.working_copy`` (iiie)
* Make ``require.sysctl`` robust to procps start failure


Version 0.15.0 (2013-07-25)
---------------------------

* Fix missing import in ``user.local_home_directory()`` (Sebastien Beal)
* Improved Arch Linux support:
    * Fix locale support in Arch Linux (Bruno Adele)
    * Add support for yaourt package manager in Arch Linux (Bruno Adele)
* Improvements to the ``redis`` module:
    * Fix Redis startup after reboot (Victor Perron)
    * Upgrade default Redis version to 2.6.14
* Improvements to the ``git`` module:
    * Add optional force parameter to git pull and checkout (Sebastien Beal)
* Improvements to the ``python`` module:
    * Add parameter to use a specific Python interpreter (Bruno Adele)
    * Stop using PyPI mirrors now that it has a CDN (Dominique Lederer)
* Debian/Ubuntu improvements:
    * Add optional version parameter to deb.install() (Anthony Scalisi)
    * Improved support for installing APT public keys (Santiago Mola)
* SmartOS improvements (Andreas Kaiser):
    * Fix md5sum on recent SmartOS
    * Fix bug in pkg.is_installed with certain package names
    * Add support for SmartOS in remote system identification
    * Add support for SmartOS in require.git.command()
* RedHat improvements:
    * Fix broken rpm.install() (Sho Shimauchi)
* Oracle JDK improvements:
    * Upgrade default version to 7u25-b15 (Sebastien Beal)
    * Fix Oracle JDK version parsing when OpenJDK is installed
    * Fix Oracle JDK installation on Debian squeeze (Stéphane Klein)
* Better tests documentation (thanks to Stéphane Klein)
* Add require.directories() (Edouard de Labareyre)
* Add support for Apache web server (Stéphane Klein)
* Upgrade default Node.js version to 0.10.13

Version 0.14.0 (2013-05-22)
---------------------------

Note: Fabtools now requires Fabric >= 1.6.0

* Upgrade default pip version to 1.3.1
* Improved vagrant support:
    * Add support for Vagrant 1.1 providers in functional tests
    * Also set ``env.user`` and ``env.hosts`` in ``vagrant`` context manager
* Add ``fabtools.system.cpus`` to get the host's CPU count
* Less verbose output
* Move OS detection functions to ``fabtools.system``
* Better support for Red Hat based systems
* Improvements to the ``user`` module:
    * Fix home dir default behaviour in ``require.user``
    * Add support for SSH authorized keys (Kamil Chmielewski)
    * Add support for SSH known hosts public keys
    * Add ``non_unique`` argument to user functions (Zhang Erning)
    * Get absolute path to the local user's home dir (Sebastien Beal)
* Use ``SHOW DATABASES`` to test existence of MySQL (Zhang Erning)
* Improvements to the ``git`` module
    * Expose lower level ``fetch`` operation (Andreas Kaiser)
    * Fix missing import in ``require`` module (Muraoka Yusuke)
    * Require ``git`` command line tool
* Use ``ifconfig`` as root in ``network`` module
* Update OpenVZ guest context manager for Fabric 1.6.0
* Improvements to the ``python`` module:
    * Improved detection of distribute
    * Add support for virtualenv ``--prompt`` option (Artem Nezvigin)
    * Allow relative path in ``virtualenv`` context manager
* Improvements to the ``oracle_jdk`` module:
    * Upgrade default Oracle JDK version to 7u21-b11 (Kamil Chmielewski)
    * Add support for Oracle JDK version 6 (Sebastien Beal)
* Fix broken ``fabtools.deb.upgrade``
* Add support for Arch Linux packages (Bruno Adele)
* Add support for Linux disk partitions (Bruno Adele)
* Add OpenSSH server hardening (Adam Patterson)
* Add ``systemd`` module (Jakub Stasiak)
* Improvements to the ``redis`` module:
    * Fix broken Redis configuration (Victor Perron)
    * Upgrade default Redis version to 2.6.13
* Abort on nginx configuration errors
* Upgrade default Node.js version to 0.10.7

Version 0.13.0 (2013-03-15)
---------------------------

* Add support for managing remote git repositories (Andreas Kaiser)
* Add intersphinx to docs (Andreas Kaiser)
* Add HTTP proxy support to speed up functional tests
* Upgrade default Node.js version to 0.10.0
* Upgrade default Redis version to 2.6.11
* Upgrade default Oracle JDK version to 7u17-b02
* Fix vagrant support (thanks to Dominique Lederer and anentropic)

Version 0.12.0 (2013-03-04)
---------------------------

* Do not create home directory for system users
* Fix ``pkg.is_installed`` on SmartOS (thanks to Anthony Scalisi)
* Fix ``system.get_arch`` (thanks to Kamil Chmielewski)
* Add support for installing Oracle JDK (thanks to Kamil Chmielewski)
* Add support for creating Postgres schemas (thanks to Michael Bommarito)
* Fix ``mysql.user_exists`` (thanks to Serge Travin)

Version 0.11.0 (2013-02-15)
---------------------------

* Fix requiring an existing user (thanks to Jonathan Peel)
* Upgrade default Redis version to 2.6.10
* Upgrade default Node.js version to 0.8.19
* Better support for remote hosts where sudo is not installed

Version 0.10.0 (2013-02-12)
---------------------------

* Enable/disable nginx sites (thanks to Sébastien Béal)
* Add support for SmartOS (thanks to Anthony Scalisi)
* Add support for RHEL/CentOS/SL (thanks to Anthony Scalisi)

Version 0.9.4 (2013-01-10)
--------------------------

* Add files missing in 0.9.3 (thanks to Stéfane Fermigier)

Version 0.9.3 (2013-01-08)
--------------------------

* Fix bugs in user creation (thanks pahaz and Stéphane Klein)
* Add support for group creation

Version 0.9.2 (2013-01-05)
--------------------------

* Add syntax highlighting in README (thanks to Artur Dryomov)

Version 0.9.1 (2013-01-04)
--------------------------

* Fix documentation formatting issues

Version 0.9.0 (2013-01-04)
--------------------------

* Improve user creation and modification
* Add support for BSD / OS X to ``files.owner``, ``files.group``,
  ``files.mode`` and ``files.md5sum`` (thanks to Troy J. Farrell)
* Improve PostgreSQL user creation (thanks to Troy J. Farrell
  and Axel Haustant)
* Add ``reload`` and ``force_reload`` operations to the ``service``
  module (thanks to Axel Haustant)
* Fix missing import in ``require.redis`` (thanks to svevang
  and Sébastien Béal)
* Add ``clear`` option to Python virtualenv (thanks to pahaz)
* Upgrade default Redis version to 2.6.7
* Upgrade default Node.js version to 0.8.16
* Decrease verbosity of some operations
* Speed up functional tests

Version 0.8.1 (2012-10-26)
--------------------------

* Really fix pip version parsing issue
* Upgrade default pip version to 1.2.1

Version 0.8.0 (2012-10-26)
--------------------------

* Improve user module (thanks to Gaël Pasgrimaud)
* Fix locale support on Debian (thanks to Olivier Kautz)
* Fix version number in documentation (thanks to Guillaume Ayoub)
* Fix potential issue with pip version parsing

Version 0.7.0 (2012-10-13)
--------------------------

* Fix changed directory owner requirement (thanks to Troy J. Farrell)
* Add functions to get a file's owner, group and mode

Version 0.6.0 (2012-10-13)
--------------------------

* Add support for Node.js (thanks to Frank Rousseau)
* Fix dependency on Fabric >= 1.4.0 (thanks to Laurent Bachelier)

Version 0.5.1 (2012-09-21)
--------------------------

* Documentation and packaging fixes

Version 0.5 (2012-09-21)
------------------------

* The ``watch`` context manager now allows you to either provide
  a callback or do an explicit check afterwards (**warning**: this change
  is not backwards compatible, please update your fabfiles)
* Add support for some network-related operations:
    * get the IPV4 address assigned to an interface
    * get the list of name server IP addresses
* The ``services`` module now supports both upstart and traditional
  SysV-style ``/etc/init.d`` scripts (thanks to Selwin Ong)
* The ``virtualenv`` context manager can now also be used with ``local()``
  (thanks to khorn)
* The ``supervisor`` module now uses ``update`` instead of ``reload``
  to avoid unnecessary restarts (thanks to Dan Fairs)
* Add support for OpenVZ containers (requires a kernel with OpenVZ patches)
* ``pip`` can now use a download cache
* Upgrade Redis version to 2.4.17
* Misc bug fixes and improvements
* Support for Ubuntu 12.04 LTS and Debian 6.0
* Documentation improvements

Version 0.4 (2012-05-30)
------------------------

* Added support for requiring an arbitrary APT source
* Added support for adding APT signing keys
* Added support for requiring a user with a home directory
* Added vagrant helpers
* Fixed Python virtualenv context manager

Version 0.3.2 (2012-03-19)
--------------------------

* Fixed README formatting

Version 0.3.1 (2012-03-19)
--------------------------

* Fixed bug in functional tests runner

Version 0.3 (2012-03-19)
------------------------

* Added support for Shorewall (Shoreline Firewall)
* Fixed Python 2.5 compatibility
* Refactored tests

Version 0.2.1 (2012-03-09)
--------------------------

* Packaging fixes

Version 0.2 (2012-03-09)
------------------------

* Added support for hostname and sysctl (kernel parameters)
* Added support for Redis
* Simplified API for supervisor processes

Version 0.1.1 (2012-02-19)
--------------------------

* Packaging fixes

Version 0.1 (2012-02-19)
------------------------

* Initial release
