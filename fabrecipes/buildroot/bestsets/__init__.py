# Library

# Fabric
from fabric.api import settings, task, hide

# Fabtools
from fabric.api import cd
from fabtools import require
from fabric.contrib.files import sed


@task
def install(target):
    """
    Install bestset script from open-console

    Ex: fab -H root@192.168.1.1 install:target=recalbox
    """

    # Set default directories
    if target == "recalbox":
        dstdir = '/recalbox/share'
        rompath = '/recalbox/share/roms/'
    else:
        dstdir = '~'
        rompath = '/home/pi/RetroPie/roms'

    # Download the script
    with cd(dstdir):
        with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
            require.file(
                url='https://raw.githubusercontent.com/frthery/ES_RetroPie/master/oc_bestsets_downloader/oc_bestsets_downloader.sh',
                mode=755
            )
        sed('oc_bestsets_downloader.sh', "ROM_PATH=.*", "ROM_PATH=%s" % rompath)
