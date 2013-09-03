import os

# Fabric
from fabric.api import env, task
from fabric.operations import put
# Fabtools
from fabtools.utils import run_as_root
from fabtools import require
from fabtools import python

# Fabrecipes
from fabrecipes.commons import dotfiles
"""
   This script install emacs with :
   - Installation in virtualenv with Python2
   - el.get feature
"""


@task
def install_p2k():
    """
    Install emacs with some features in python 2.7 environement
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

    python_cmd = 'python2.7'
    virtualenv = '.virtualenvs/emacs_p2k'
    require.python.pip(python_cmd=python_cmd)
    require.python.package(
        'virtualenv',
        python_cmd=python_cmd,
        use_sudo=True,
    )
    require.python.package(
        'virtualenvwrapper',
        python_cmd=python_cmd,
        use_sudo=True,
    )
    require.python.virtualenv(
        virtualenv,
        python_cmd=python_cmd,
        venv_python='python2.7',
    )

    with python.virtualenv(virtualenv):
        here = os.path.dirname(__file__)
        requirements = '%(here)s/requirements.txt' % locals()
        put(requirements, '/tmp/requirements.txt')
        require.python.requirements(
            '/tmp/requirements.txt',
        )

    # Synchronize user
    dotfiles.sync('fabrecipes/emacs/emacs_p2k/user/', '$HOME/')
    dotfiles.sync('fabrecipes/emacs/emacs_p2k/sys/', '/', use_sudo='true')
