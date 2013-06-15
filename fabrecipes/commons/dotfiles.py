# Fabric
from fabric.api import env, task, sudo, run

# Fabtools
from fabtools.utils import run_as_root
from fabtools.files import is_dir, is_link


@task
def fetch(repository):
    """
    Clone dotfiles project to ~/dotfiles
    """
    cloned = False
    # Check project is already cloned

    if not is_dir('$HOME/dotfiles'):
        cmd = 'cd ; git clone %(repository)s' % locals()
        run(cmd)
        cloned = True

    # Pull dotfiles project
    if not cloned:
        # Mise a jours des sources
        cmd = 'cd $HOME/dotfiles ; git pull'
        run(cmd)


@task
def sync(src, dst, use_sudo='false'):
    """
    Copy file from dotfiles dot dst
    """
    use_sudo = use_sudo.lower() == 'true'

    # Synchronize system
    dotfiles = '$HOME/dotfiles' 
    cmd = 'rsync -avr --exclude ".git/" %(dotfiles)s/%(src)s %(dst)s' % locals()
    print(cmd)
