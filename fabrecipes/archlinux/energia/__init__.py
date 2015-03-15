import os

# Fabric
from fabric.api import env, task, run
from fabric.operations import put
from fabric.context_managers import cd

# Fabtools
from fabtools.files import is_dir
from fabtools import require

"""
   Install energia toolchain developpement kit
"""


@task
def install():
    """
    Install a energia toolchain developpement kit
    """

    if not env.host_string:
        env.host_string = 'localhost'

    # Install package
    pkgs = [
        'energia',
    ]
    require.arch.packages(pkgs)

    # Install udev
    ruled = 'ATTRS{idVendor}=="0451", ATTRS{idProduct}=="c32a", MODE="0660", GROUP="users", \
RUN+="/sbin/modprobe ftdi-sio" RUN+="/bin/sh -c \'/bin/echo 0451 c32a > /sys/bus/usb-serial/drivers/ftdi_sio/new_id\''
    require.file('/etc/udev/rules.d/energia.rules', contents=ruled, use_sudo=True)
