Changelog
=========

Version 0.9.0 (2013-01-04)
--------------------------

* Improve user creation and modification
* Add support for BSD / OS X to `files.owner`, `files.group`,
  `files.mode` and `files.md5sum` (thanks to Troy J. Farrell)
* Improve PostgreSQL user creation (thanks to Troy J. Farrell
  and Axel Haustant)
* Add `reload` and `force_reload` operations to the `service`
  module (thanks to Axel Haustant)
* Fix missing import in `require.redis` (thanks to svevang
  and Sébastien Béal)
* Add --clear option to Python virtualenv (thanks to pahaz)
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
