# Library
import os

# Fabric
from fabric.api import settings, task, env, run, hide
from fabric.operations import put

# Fabtools
from fabtools import openwrt
from fabtools import require
from fabtools import disk

"""
OpenWrt Data to USB stick
"""


@task
def install():
    """
    If you have a USB router, you can move data to USB stick for free RAM
    This USB stick must have 3 partitions
      cfdisk /dev/usbdisk
      mkfs.ext4 /dev/usbdisk1
      mkfs.ext4 /dev/usbdisk2
      mkswap /dev/usbdisk3
    """

    # Set Shell environment
    env.shell = "/bin/ash -l -c"

    # Install USB required packages
    openwrt.update_index()
    openwrt.install([
        'openssh-sftp-server',
        'kmod-usb-storage',
        'block-mount',
        'kmod-fs-ext4',
    ])

    # Prepare system
    require.files.directory('/mnt/tmp')
    require.files.directory('/mnt/var')

    # Refresh file system
    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        run('ls -alh /mnt')

    # Mount partitions
    disk.mount('/dev/sda1', '/mnt/tmp')
    disk.mount('/dev/sda2', '/mnt/var')
    disk.swapon('/dev/sda3')

    # Copy /etc/config/fstab
    lpath = os.path.join(os.path.dirname(__file__), 'fstab')
    put(lpath, '/etc/config/fstab')
    run('/etc/init.d/fstab enable')

    # Copy /etc/init.d/data2usb
    lpath = os.path.join(os.path.dirname(__file__), 'data2usb')
    put(lpath, '/etc/init.d/data2usb')
    run('chmod +x /etc/init.d/data2usb')
    run('/etc/init.d/data2usb enable')
    run('/etc/init.d/data2usb start')
