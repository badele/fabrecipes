# Library

# Fabric
from fabric.api import settings, task, sudo, env, run
from fabric.operations import put
from fabric.api import cd

# Fabtools
from fabtools import require
from fabtools.utils import run_as_root
from fabtools.files import watch, is_dir, is_link, is_file


"""
   Install home assistant in debian wheezy and Raspberry PI wheezy
"""


@task
def install():
    """
    Install home assistant in debian wheezy and Raspberry PI wheezy
    """

    # Requirement platform
    require.deb.packages([
        'libncurses-dev', 'libreadline-dev', 'tk-dev',
        'libsqlite3-dev', 'sqlite3',
        'libgdbm-dev', 'libssl-dev',
        'libbz2-dev', 'libexpat1-dev', 'liblzma-dev', 'zlib1g-dev',
        'wget',
    ])

    # Download python3
    getfile = 'Python-3.4.3.tar.xz'
    dst = '/tmp/%s' % getfile
    if not is_file(dst):
        run_as_root(
            'wget "https://www.python.org/ftp/python/3.4.3/%s" -O %s' % (
                getfile,
                dst,
            )
        )
    with cd('/tmp'):
        run_as_root('tar xvfJ Python-3.4.3.tar.xz')

    # Install python
    with cd('/tmp/Python-3.4.3'):
        run_as_root('./configure')
        run_as_root('make')
        run_as_root('make install')

    run_as_root('rm -rf "/tmp/Python-3.4.3"')
    run_as_root('rm "/tmp/Python-3.4.3.tar.xz"')