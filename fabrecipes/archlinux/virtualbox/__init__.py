# Fabric
from fabric.api import task
from fabric.colors import red

# Fabtools
from fabtools import systemd
from fabtools import require

# Fabrecipes
from fabrecipes.commons import dotfiles

"""
   This script install virtualbox
"""


@task
def install():
    """
    Install virtualbox and use dkms virtual host modules
    """

    pkgs = [
        'virtualbox',
        'virtualbox-host-dkms',
        'linux-headers',
    ]

    # Install packages
    require.arch.packages(pkgs)

    # active startup virtualbox module compilation
    systemd.start('dkms')
    systemd.enable('dkms')

    # Synchronize user
    dotfiles.sync('fabrecipes/virtualbox/user/', '$HOME/')
    dotfiles.sync('fabrecipes/virtualbox/sys/', '/', use_sudo='true')

    print(red('Please reboot your system for use new kernel'))
