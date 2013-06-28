# Fabric
from fabric.api import task, sudo

# Fabtools
from fabric.contrib.files import append
from fabtools import require
from fabtools import arch

"""
   This script install archzfs
"""


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
