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
   Install rstblog
"""


@task
def install():
    """
    Install a rstblog in python2 virtualenv
    """
    if not env.host_string:
        env.host_string = 'localhost'

    pkgs = [
        'python2',
        'git',
    ]
    require.arch.packages(pkgs)

    project_root = '$HOME/projects'
    project_name = 'rstblog'
    use_python = 'python2.7'
    virtualenv = '.virtualenvs/rstblog'
    gitproject = 'https://github.com/badele/rstblog.git'

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

    # Get a rstblog from my repository https://github.com/badele/rstblog.git
    cloned = False
    project = '%s/%s' % (project_root, project_name)
    if not is_dir(project):
        require.files.directory(project_root)
        cmd = 'cd %(project_root)s ; git clone %(gitproject)s' % locals()
        run(cmd)
        cloned = True

    if not cloned and not is_dir(project):
        cmd = 'cd (%project)s ; git pull' % locals()
        run(cmd)


    # Install rstblog
    with python.virtualenv(virtualenv):
        here = os.path.dirname(__file__)
        requirements = '%(here)s/requirements.txt' % locals()
        put(requirements, '/tmp/requirements.txt')
        require.python.requirements(
            '/tmp/requirements.txt',
        )

        with cd(project):
            run('python2 setup.py install')
