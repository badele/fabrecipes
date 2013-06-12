import os

# Fabric
from fabric.api import settings, env, task, sudo
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

#from computer import *

"""
   This script install emacs with :
   - Installation in virtualenv with Python3
   - el.get feature
"""


@task
def install_p2k():
    """
    Install base system
    """
    if 'pkgs' not in env:
        env.pkgs = []

    pkgs = [
        'python2',
        'git',
        'mercurial',
        'emacs',
        # For flymake
        'xmlstarlet',
        'csslint-git',
    ]
    require.arch.packages(pkgs)

    use_python = 'python2.7'
    virtualenv = '.virtualenvs/emacs_p2k'
    require.python.pip(use_python=use_python)
    require.python.package(
        'virtualenv',
        use_python=use_python,
        use_sudo=True,
    )
    require.python.package(
        'virtualenvwrapper',
        use_python=use_python,
        use_sudo=True,
    )
    require.python.virtualenv(
        virtualenv,
        use_python=use_python,
        python='python2.7',
    )

    with python.virtualenv(virtualenv):
        here = os.path.dirname(__file__)
        requirements = '%(here)s/requirements.txt' % locals()
        put(requirements, '/tmp/requirements.txt')
        require.python.requirements(
            '/tmp/requirements.txt',
        )

    # Synchronize user
    require.files.directory('.emacs_p2k')
    put('%(here)s/user/.emacs_p2k.el' % locals(),
        '~/.emacs_p2k/.emacs.el',
        )

    # Synchronize system
    put('%(here)s/system/usr/local/bin/my_emacs_p2k' % locals(),
        '/usr/local/bin',
        use_sudo=True,
        )
    run_as_root('chown root:root /usr/local/bin/my_emacs_p2k && chmod 0755 /usr/local/bin/my_emacs_p2k')
