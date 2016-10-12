# Keep imports sorted alphabetically
import fabtools.require.arch
import fabtools.require.apache
import fabtools.require.conda
import fabtools.require.curl
import fabtools.require.deb
import fabtools.require.docker
import fabtools.require.files
import fabtools.require.git
import fabtools.require.mercurial
import fabtools.require.mysql
import fabtools.require.nginx
import fabtools.require.nodejs
import fabtools.require.openvz
import fabtools.require.opkg
import fabtools.require.oracle_jdk
import fabtools.require.pkg
import fabtools.require.portage
import fabtools.require.postfix
import fabtools.require.postgres
import fabtools.require.python
import fabtools.require.redis
import fabtools.require.rpm
import fabtools.require.service
import fabtools.require.shorewall
import fabtools.require.supervisor
import fabtools.require.system
import fabtools.require.tomcat
import fabtools.require.users

from fabtools.require.files import (
    directory,
    file,
)
from fabtools.require.users import (
    user,
    sudoer,
)
from fabtools.require.groups import group
