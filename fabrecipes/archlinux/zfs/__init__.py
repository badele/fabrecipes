# Library
import datetime

# Fabric
from fabric.api import settings, task, sudo, env, hide
from fabric.colors import red, green

# Fabtools
from fabric.contrib.files import append
from fabtools.files import is_dir
from fabtools import require
from fabtools import arch
"""
   This script install archzfs
"""

# cryptsetup luksFormat -c aes-xts-plain64 -s 512  /dev/sdb1
# cryptsetup luksOpen  /dev/sdb1 mapname

# zpool create POOLNAME /dev/mapper/mapname

# zfs create POOLNAME/documents
# zfs set compress=on POOLNAME/documents
# zfs set dedup=on POOLNAME/documents


@task
def install():
    """
    Install zfs from archzfs (demizerone repository)
    """

    # Add archzfs repository
    config_file = '/etc/pacman.conf'
    append(config_file, '[demz-repo-core]')
    append(config_file, 'Server = http://demizerone.com/$repo/$arch')

    # Add key
    sudo('pacman-key -r 0EE7A126')
    sudo('pacman-key --lsign-key 0EE7A126')

    # Update the package database
    arch.update_index()

    # Install package
    require.arch.package('archzfs')


def create(zfs_name):
    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        res = sudo('zfs create %s' % zfs_name)
        if not res.succeeded:
            print(red("Can't create filesystem %s" % zfs_name))


def require_filesystem(zfs_name):
    if not env.host_string:
        env.host_string = 'localhost'

    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        res = sudo('zfs list -H -o name | grep "^%s$"' % zfs_name)
        if not res.succeeded:
            create(zfs_name)


def bk_list(zfs_name):
    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        res = sudo('zfs list -H -r -d1 -t snap -s name -o name %s | egrep  "@[0-9]{4}" ' % zfs_name)
        return [line.split('@') for line in res.splitlines()]


@task
def check_snapshot(zfs_name):
    if not env.host_string:
        env.host_string = 'localhost'

    snapshot = '%s@%s' % (zfs_name, today())

    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        sudo('zfs list -H -t snap -o name | grep "%s"' % snapshot)


@task
def backup(zfs_name):
    """
    Create a today snap for the zfs_name filesystem

    fab backup:zfs_name
    """

    if not env.host_string:
        env.host_string = 'localhost'

    now = today()
    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):   
        res = sudo('zfs list -r -t snap -o name -s name %s | grep \'%s\'' % (zfs_name, now))
        if not res.succeeded:
            res = sudo('zfs snapshot -r %s@%s' % (zfs_name, now))
            if res.succeeded:
                print(green("Backup done for %s@%s" % (zfs_name, now)))


@task
def replicate(zfs_src,zfs_dst):
    """
    replicate snapshot to another pool

    fab replicate:zfs_src,zfs_dst
    """

    if not env.host_string:
        env.host_string = 'localhost'

    require_filesystem('%s/replicated' % zfs_dst)
    require_filesystem('%s/replicated/USB_140' % zfs_dst)

    now = today()
    slocal = bk_list(zfs_src)
    sremote = bk_list(zfs_dst)
    sudo('zfs send -R %s@%s | zfs recv -Fduv %s/replicated/%s' % (
        slocal[0][0],
        slocal[0][1],
        zfs_dst,
        slocal[0][0],
    )
    )


def today():
    now = datetime.datetime.now()
    return str(now)[:10]
