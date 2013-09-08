# Library
import datetime

# Fabric
from fabric.api import settings, task, sudo, env, hide, abort
from fabric.colors import red, green, yellow

# Fabtools
from fabric.contrib.files import append
from fabtools import require
from fabtools import arch
from fabtools import disk

# Fabrecipes
from fabrecipes.commons import dotfiles

"""
   This script install archzfs and add another features
   - Install ZFS for archlinux
   - Make a snapshot from your LIVE HDD (working HDD)
   - Replicate your LIVE working HDD to BACKUP HDD

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
    append(config_file, '[demz-repo-core]', use_sudo=True)
    append(config_file, 'Server = http://demizerone.com/$repo/$arch', use_sudo=True)

    # Add key
    sudo('pacman-key -r 0EE7A126')
    sudo('pacman-key --lsign-key 0EE7A126')

    # Update the package database
    arch.update_index()

    # Install package
    require.arch.package('archzfs')

    # Synchronize user
    dotfiles.sync('fabrecipes/zfs/user/', '$HOME/')
    dotfiles.sync('fabrecipes/zfs/sys/', '/', use_sudo='true')


def create(zfs_name):
    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        res = sudo('zfs create -p %s' % zfs_name)
        if not res.succeeded:
            print(red("Can't create filesystem %s" % zfs_name))


def require_zfs(zfs_name):
    if not env.host_string:
        env.host_string = 'localhost'

    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        res = sudo('zfs list -H -o name | grep "^%s$"' % zfs_name)
        if not res.succeeded:
            create(zfs_name)


@task
def init_crypted_zfs(device, zfs_name):
    """
    Prepare hhd backup from live HDD
    ex:
      fab init_crypted_zfs:/dev/sdb,backup
    """
    if not env.host_string:
        env.host_string = 'localhost'

    # Check a first partition is in Solaris (for security format)
    ptype = disk.partitions(device)
    partition = '%s1' % device
    if ptype[partition] != 0xBF:
        abort("The first partition is not SOLARIS type (0xBF)")

    # Prepare a crypted ZFS disk
    sudo('cryptsetup luksFormat -c aes-xts-plain64 -s 512 %s' % partition)
    sudo('cryptsetup luksOpen %s %s' % (partition, zfs_name.lower()))
    sudo('zpool create %s /dev/mapper/%s' % (zfs_name.upper(), zfs_name.lower()))
    sudo('zfs set compress=on %s' % zfs_name.upper())


def ds_list(zfs_name):
    """
    Get a dataset list
    """
    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        res = sudo('zfs list -H -d1 -t filesystem %s' % zfs_name)
        return [line.split('\t')[0].replace('%s/' % zfs_name,'',1) for line in res.splitlines()[1:]]


def bk_list(zfs_name):
    """
    Get a backup snapshot list
    """
    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        res = sudo('zfs list -H -d1 -t snap -s name -o name %s | egrep  "@[0-9]{4}" ' % zfs_name)
        return [line.split('@')[1] for line in res.splitlines()]


@task
def bk_snapshots(pool_name="LIVE"):
    """
    Create a today snap for the zfs_name filesystem

    fab backup:pool_name
    """

    if not env.host_string:
        env.host_string = 'localhost'

    sdslist = ds_list(pool_name)
    for ds in sdslist:
        bk_snapshot('%s/%s' % (pool_name, ds))


def bk_snapshot(ds_name):
    """
    Create a today snap for the zfs_name filesystem

    fab backup:zfs_name
    """

    if not env.host_string:
        env.host_string = 'localhost'

    now = today()
    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        res = sudo('zfs list -r -t snap -o name -s name %s | grep \'%s\'' % (ds_name, now))
        if not res.succeeded:
            res = sudo('zfs snapshot %s@%s' % (ds_name, now))
            if res.succeeded:
                print(green("Snapshot done for %s@%s" % (ds_name, now)))
            else:
                print(red("Problem with snapshot %s@%s" % (ds_name, now)))
        else:
            print(yellow("Snapshot %s@%s already exist" % (ds_name, now)))


@task
def bk_keep_snapshots(zfs_name="LIVE", nb_keep=15):
    """
    Keep only nb snapshot

    fab bk_keep_snapshot
    """

    if not env.host_string:
        env.host_string = 'localhost'

    # Check if dataset exist on destination
    sdslist = ds_list(zfs_name)
    for ds in sdslist:
        print("search for %s" % ds)
        bklist = bk_list('%s/%s' % (zfs_name, ds))
        lastpos = len(bklist) - nb_keep
        todelete = bklist[:lastpos]
        for bk in todelete:
            bk_delete_snapshot('%s/%s@%s' % (zfs_name, ds, bk))


def bk_delete_snapshot(snap_name):
    sudo('zfs destroy %s' % snap_name)


@task
def bk_replicate(nb_keep=15, zfs_src="LIVE", zfs_dst="BACKUP", path=""):
    """
    replicate snapshot to another pool

    fab replicate:zfs_src,zfs_dst
    """

    if not env.host_string:
        env.host_string = 'localhost'

    dst_path = "%s%s" % (zfs_dst, path)
    require_zfs('%s' % dst_path)

    sdslist = ds_list(zfs_src)
    dbklist = ds_list(zfs_dst)

    # Check if dataset exist on destination
    for ds in sdslist:
        if ds not in dbklist:
            create('%s/%s' % (dst_path, ds))

    # Replicate
    for ds in sdslist:
        print("backup for %s" % ds)
        sbklist = bk_list('%s/%s' % (zfs_src, ds))
        dbklist = bk_list('%s/%s' % (zfs_dst, ds))

        # Check if the zfs_src have the snapshot
        if len(sbklist) == 0:
            abort("Please execute fab bk_snapshot:%s before bk_replicate" % zfs_src)

        # # Check if first replication
        if len(dbklist) == 0:
            firstbk = sbklist[0]
            firstpath = '%s/%s@%s' % (zfs_src, ds, firstbk)
            sudo('zfs send -vD %s | zfs recv -Fduv %s' % (
                firstpath,
                dst_path,
            )
            )

        # If LIVE have more one backups
        if len(sbklist) > 1:
            pos = 0
            for bk in sbklist[:-1]:
                firstbk = bk
                nextbk = sbklist[pos + 1]
                recalc_dbklist = bk_list('%s/%s' % (zfs_dst, ds))
                if firstbk in recalc_dbklist:
                    if nextbk not in recalc_dbklist:
                        firstpath = '%s/%s@%s' % (zfs_src, ds, firstbk)
                        nextpath = '%s/%s@%s' % (zfs_src, ds, nextbk)
                        sudo('zfs send -vi %s %s | zfs recv -Fduv %s' % (
                            firstpath,
                            nextpath,
                            dst_path,
                        )
                        )
                pos += 1

    # Delete snapshot if not in LIVE pool
    for ds in sdslist:
        sbklist = bk_list('%s/%s' % (zfs_src, ds))
        dbklist = bk_list('%s/%s' % (zfs_dst, ds))
        for dbk in dbklist:
            if dbk not in sbklist:
                bk_delete_snapshot('%s/%s@%s' % (zfs_dst, ds, dbk))




def today():
    now = datetime.datetime.now()
    return str(now)[:16].replace(' ', '_')
