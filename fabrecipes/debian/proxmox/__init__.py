# Library

# Fabric
from fabric.api import settings, task, sudo, env, run

# Fabtools
from fabtools import service


"""
   Promox tools

"""


@task
def recreate_pvedata(dirsave, size):
    """
    Recreate the pve-data with the defined size
    """

    # Stop service
    service.stop('pvedaemon')
    service.stop('vz')
    service.stop('qemu-server')

    # Backup the /var/lib/vz
    run('tar -czf %s/vz.tgz /var/lib/vz' % dirsave)

    # Delete the pve-data
    run('umount /var/lib/vz')
    run('lvremove /dev/pve/data')

    # Create the new pve-data
    run('lvcreate -n data -L %s pve' % size)
    run('mkfs.ext3 /dev/mapper/pve-data')
    run('mount /dev/mapper/pve-data /var/lib/vz')

    # Restore the Backup /var/lib/vz
    run('tar -xzf %s/vz.tgz -C /' % dirsave)

    # Start service
    service.start('qemu-server')
    service.start('vz')
    service.start('pvedaemon')


# @task 
# def extend_pve(pdisk):
#     run('pvcreate %s' % pdisk)
#     run('vgextend pve %s' % pdisk)
