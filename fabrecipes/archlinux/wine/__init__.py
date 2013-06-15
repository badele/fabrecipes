import os

# Fabric
from fabric.api import settings, env, task, sudo, run, local
from fabric.utils import abort
from fabric.colors import red
from fabric.operations import prompt, reboot, put

# Fabtools
from fabtools.require import file as require_file
from fabtools.utils import run_as_root
from fabric.contrib.files import append, comment, uncomment, sed
from fabtools.files import watch, is_dir, is_link
from fabtools import require
from fabtools import python
from fabtools import system
from fabtools import arch
from fabtools import disk

# Fabrecipes
from fabrecipes.commons import dotfiles

"""
   This script install wine with :
   - install required libraries
   - configure wine
   - install firefox 11
   - install flash player 11
"""


@task
def install():
    """
    Install wine with customization
    """
    if 'pkgs' not in env:
        env.pkgs = []

    pkgs = [
        'wine',
        'wine_gecko',
        'wine-mono',
        'winetricks-svn',
        'lib32-libxml2',
        'lib32-mpg123',
        'lib32-giflib',
        'lib32-libpng',
        'lib32-gnutls',
    ]
    require.arch.packages(pkgs)

    run('winecfg')
    cmd = 'WINEPREFIX=/home/badele/.wine winetricks firefox flash11'
    run('DISPLAY=:0 %s' % cmd)

print("IMPORTED wine")
