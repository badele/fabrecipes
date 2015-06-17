import inspect
from re import escape

# Fabric
from fabric.api import settings, env, task, sudo, run
from fabric.utils import abort
from fabric.colors import red
from fabric.operations import prompt, reboot
from fabric.contrib.files import append, comment, uncomment, sed

# Fabtools
from fabtools.require import file as require_file
from fabtools.utils import run_as_root
from fabtools.files import watch, is_dir, is_link, is_file
from fabtools import arch
from fabtools import disk
from fabtools import python
from fabtools import require
from fabtools import systemd
from fabtools import system
from fabtools import user

# Fabrecipes
from fabrecipes.commons import dotfiles

@task
def prepare_sdhc(device):
    """
    Prepare de SDHC for installing ArchlinuxARM
    """

    if not env.host_string:
        env.host_string = 'localhost'

    # require package for prepare SDHC
    require.arch.packages([
        'wget',
        'p7zip',
    ]
    )

    getfile = 'ArchLinuxARM-rpi-latest.zip'
    dst = '/tmp/%s' % getfile
    if not is_file(dst):
        run(
            'wget "http://archlinuxarm.org/os/%s" -O %s' % (
                getfile,
                dst,
            )
        )
