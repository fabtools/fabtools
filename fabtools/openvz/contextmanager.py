"""
OpenVZ containers
=================
"""

from contextlib import contextmanager
import hashlib
import os
import posixpath
import tempfile

from fabric.api import (
    env,
    hide,
    output,
    settings,
    sudo,
)
from fabric.operations import (
    _AttributeString,
    _execute,
    _prefix_commands,
    _prefix_env_vars,
    _shell_wrap,
    _sudo_prefix,
)
from fabric.state import default_channel
from fabric.utils import error
import fabric.operations
import fabric.sftp

from fabric.context_managers import (
    quiet as quiet_manager,
    warn_only as warn_only_manager,
)


@contextmanager
def guest(name_or_ctid):
    """
    Context manager to run commands inside a guest container.

    Supported basic operations are: `run`_, `sudo`_ and `put`_.

    .. warning:: commands executed with ``run()`` will be run as
                 **root** inside the container.
                 Use ``sudo(command, user='foo')`` to run them as
                 an unpriviledged user.

    Example::

        from fabtools.openvz import guest

        with guest('foo'):
            run('hostname')
            sudo('whoami', user='alice')
            put('files/hello.txt')

    .. _run: http://docs.fabfile.org/en/1.4.3/api/core/operations.html#fabric.operations.run
    .. _sudo: http://docs.fabfile.org/en/1.4.3/api/core/operations.html#fabric.operations.sudo
    .. _put: http://docs.fabfile.org/en/1.4.3/api/core/operations.html#fabric.operations.put
    """

    # Monkey patch fabric operations
    _orig_run_command = fabric.operations._run_command
    _orig_put = fabric.sftp.SFTP.put

    def run_guest_command(command, shell=True, pty=True, combine_stderr=True,
                          sudo=False, user=None, quiet=False, warn_only=False,
                          stdout=None, stderr=None, group=None, timeout=None):
        """
        Run command inside a guest container
        """

        # Use a non-login shell
        _orig_shell = env.shell
        env.shell = '/bin/bash -c'

        # Use double quotes for the sudo prompt
        _orig_sudo_prefix = env.sudo_prefix
        env.sudo_prefix = 'sudo -S -p "%(sudo_prompt)s" '

        # Try to cd to the user's home directory for consistency,
        # as the default directory is "/" with "vzctl exec2"
        if not env.cwd:
            env.command_prefixes.insert(0, 'cd 2>/dev/null || true')

        # Build the guest command
        guest_command = _shell_wrap_inner(
            _prefix_commands(_prefix_env_vars(command), 'remote'),
            True,
            _sudo_prefix(user) if sudo and user else None
        )
        host_command = "vzctl exec2 %s '%s'" % (name_or_ctid, guest_command)

        # Restore env
        env.shell = _orig_shell
        env.sudo_prefix = _orig_sudo_prefix
        if not env.cwd:
            env.command_prefixes.pop(0)

        # Run host command as root
        return _run_host_command(host_command, shell=shell, pty=pty,
                                 combine_stderr=combine_stderr)

    def put_guest(self, local_path, remote_path, use_sudo, mirror_local_mode,
                  mode, local_is_path):
        """
        Upload file to a guest container
        """
        pre = self.ftp.getcwd()
        pre = pre if pre else ''
        if local_is_path and self.isdir(remote_path):
            basename = os.path.basename(local_path)
            remote_path = posixpath.join(remote_path, basename)
        if output.running:
            print("[%s] put: %s -> %s" % (
                env.host_string,
                local_path if local_is_path else '<file obj>',
                posixpath.join(pre, remote_path)
            ))

        # Have to bounce off FS if doing file-like objects
        fd, real_local_path = None, local_path
        if not local_is_path:
            fd, real_local_path = tempfile.mkstemp()
            old_pointer = local_path.tell()
            local_path.seek(0)
            file_obj = os.fdopen(fd, 'wb')
            file_obj.write(local_path.read())
            file_obj.close()
            local_path.seek(old_pointer)

        # Use temporary file with a unique name on the host machine
        guest_path = remote_path
        hasher = hashlib.sha1()
        hasher.update(env.host_string)
        hasher.update(name_or_ctid)
        hasher.update(guest_path)
        host_path = hasher.hexdigest()

        # Upload the file to host machine
        rattrs = self.ftp.put(real_local_path, host_path)

        # Copy file to the guest container
        with settings(hide('everything'), cwd=""):
            cmd = "cat \"%s\" | vzctl exec \"%s\" 'cat - > \"%s\"'" \
                % (host_path, name_or_ctid, guest_path)
            _orig_run_command(cmd, sudo=True)

        # Revert to original remote_path for return value's sake
        remote_path = guest_path

        # Clean up
        if not local_is_path:
            os.remove(real_local_path)

        # Handle modes if necessary
        if (local_is_path and mirror_local_mode) or (mode is not None):
            lmode = os.stat(local_path).st_mode if mirror_local_mode else mode
            lmode = lmode & 07777
            rmode = rattrs.st_mode & 07777
            if lmode != rmode:
                with hide('everything'):
                    sudo('chmod %o \"%s\"' % (lmode, remote_path))

        return remote_path

    fabric.operations._run_command = run_guest_command
    fabric.sftp.SFTP.put = put_guest

    yield

    # Monkey unpatch
    fabric.operations._run_command = _orig_run_command
    fabric.sftp.SFTP.put = _orig_put


@contextmanager
def _noop():
    yield


def _run_host_command(command, shell=True, pty=True, combine_stderr=True,
                      quiet=False, warn_only=False, stdout=None, stderr=None,
                      timeout=None):
    """
    Run host wrapper command as root

    (Modified from fabric.operations._run_command to ignore prefixes,
    path(), cd(), and always use sudo.)
    """
    manager = _noop
    if warn_only:
        manager = warn_only_manager
    # Quiet's behavior is a superset of warn_only's, so it wins.
    if quiet:
        manager = quiet_manager
    with manager():
        # Set up new var so original argument can be displayed verbatim later.
        given_command = command
        # Handle context manager modifications, and shell wrapping
        wrapped_command = _shell_wrap(
            command,    # !! removed _prefix_commands() & _prefix_env_vars()
            shell,
            _sudo_prefix(None)  # !! always use sudo
        )
        # Execute info line
        which = 'sudo'          # !! always use sudo
        if output.debug:
            print("[%s] %s: %s" % (env.host_string, which, wrapped_command))
        elif output.running:
            print("[%s] %s: %s" % (env.host_string, which, given_command))

        # Actual execution, stdin/stdout/stderr handling, and termination
        result_stdout, result_stderr, status = _execute(
            channel=default_channel(), command=wrapped_command, pty=pty,
            combine_stderr=combine_stderr, invoke_shell=False, stdout=stdout,
            stderr=stderr, timeout=timeout)

        # Assemble output string
        out = _AttributeString(result_stdout)
        err = _AttributeString(result_stderr)

        # Error handling
        out.failed = False
        out.command = given_command
        out.real_command = wrapped_command
        if status not in env.ok_ret_codes:
            out.failed = True
            msg = "%s() received nonzero return code %s while executing" % (
                which, status
            )
            if env.warn_only:
                msg += " '%s'!" % given_command
            else:
                msg += "!\n\nRequested: %s\nExecuted: %s" % (
                    given_command, wrapped_command
                )
            error(message=msg, stdout=out, stderr=err)

        # Attach return code to output string so users who have set things to
        # warn only, can inspect the error code.
        out.return_code = status

        # Convenience mirror of .failed
        out.succeeded = not out.failed

        # Attach stderr for anyone interested in that.
        out.stderr = err

        return out


def _shell_wrap_inner(command, shell=True, sudo_prefix=None):
    """
    Conditionally wrap given command in env.shell (while honoring sudo.)

    (Modified from fabric.operations._shell_wrap to avoid double escaping,
    as the wrapping host command would also get shell escaped.)
    """
    # Honor env.shell, while allowing the 'shell' kwarg to override it (at
    # least in terms of turning it off.)
    if shell and not env.use_shell:
        shell = False
    # Sudo plus space, or empty string
    if sudo_prefix is None:
        sudo_prefix = ""
    else:
        sudo_prefix += " "
    # If we're shell wrapping, prefix shell and space, escape the command and
    # then quote it. Otherwise, empty string.
    if shell:
        shell = env.shell + " "
        command = '"%s"' % command    # !! removed _shell_escape() here
    else:
        shell = ""
    # Resulting string should now have correct formatting
    return sudo_prefix + shell + command
