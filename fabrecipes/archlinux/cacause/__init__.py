import os

# Fabric
from fabric.api import env, task, run
from fabric.operations import put
from fabric.context_managers import cd

# Fabtools
from fabtools.files import is_dir
from fabtools import require
from fabtools import python


"""
   Install cacause
"""


@task
def install():
    """
    Install a pelican in python2 virtualenv
    """

    if not env.host_string:
        env.host_string = 'localhost'

    pkgs = [
        'python2',
        'git',
    ]
    require.arch.packages(pkgs)

    project_root = '$HOME/projects'
    project_name = 'cacause'
    use_python = 'python2.7'
    virtualenv = '.virtualenvs/cacause'
    gitproject = 'git@bitbucket.org:nadley/cacause.git'

    require.python.pip(python_cmd=use_python)
    require.python.package(
        'virtualenv',
        python_cmd=use_python,
        use_sudo=True,
    )
    require.python.package(
        'virtualenvwrapper',
        python_cmd=use_python,
        use_sudo=True,
    )
    require.python.virtualenv(
        virtualenv,
        python_cmd=use_python,
        venv_python='python2.7',
    )

    # Get a pelican github repository
    cloned = False
    project = '%s/%s' % (project_root, project_name)
    if not is_dir(project):
        require.files.directory(project_root)
        cmd = 'cd %s ; git clone %s ; cd cacause ; git checkout server' % (project_root, gitproject)
        run(cmd)
        cloned = True

    if not cloned and not is_dir(project):
        cmd = 'cd (%project)s ; git pull' % locals()
        run(cmd)


    # Install pelican
    with python.virtualenv(virtualenv):
        here = os.path.dirname(__file__)
        requirements = '%(here)s/requirements.txt' % locals()
        put(requirements, '/tmp/requirements.txt')
        require.python.requirements(
            '/tmp/requirements.txt',
        )
