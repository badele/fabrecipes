# Library

# Fabric
from fabric.api import settings, task, sudo, env, run

# Fabtools
from fabric.api import cd
from fabtools import system
from fabtools import utils
from fabtools import deb
from fabtools import require


@task
def install(version,sqlpass):
    """
    Seafile installation from the official documentation
    http://manual.seafile.com/deploy/using_mysql.html

    Ex: fab -H root@192.168.253.38 install:version=4.1.0,sqlpass=sqlpass
    """

    # Get linux architecture
    arch = system.get_arch()
    if arch == "x86_64":
        archprefix = "x86-64"
    else:
        archprefix = "i386"

    # Commons vars
    destinstall = "/opt/seafile"
    serverfile = 'seafile-server_%(version)s_%(archprefix)s.tar.gz' % locals()

    # # Up to date
    # require.deb.update_index()
    #

    # Requirements for installation
    require.deb.packages([
        'python2.7',
        'python-setuptools',
        'python-imaging',
        'python-mysqldb',
    ])

    # Install and set MySQL password
    require.mysql.server(version='5.5', password=sqlpass)

    # # Download a server file
    with cd("/tmp"):
        require.file(
            url='https://bitbucket.org/haiwen/seafile/downloads/%(serverfile)s' % locals()
        )

    # Prepare Install
    require.directory(destinstall)
    with cd(destinstall):
        utils.run_as_root('mv /tmp/seafile-server_* .')
        utils.run_as_root('tar -xvzf seafile-server_*' % locals())
        require.directory('installed')
        utils.run_as_root('mv seafile-server_* installed' % locals())

    # Install MySQL
    with cd('%(destinstall)s/seafile-server-%(version)s' % locals()):
        utils.run_as_root('./setup-seafile-mysql.sh')



