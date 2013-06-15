# Fabric
from fabric.api import env, task, sudo, run
from fabric.utils import abort

# Fabtools
#from fabtools.utils import run_as_root
from fabtools.files import is_dir
from fabric.colors import red

@task
def fetch(git):
    """
    Clone dotfiles project to ~/dotfiles
    """
    cloned = False
    # Check project is already cloned

    if not is_dir('/home/%(user)s/dotfiles' % env):
        cmd = 'cd ; git clone %(git)s' % locals()
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
    dotfiles = '/home/%(user)s/dotfiles' % env

    # Update dotfiles
    if not is_dir(dotfiles):
        abort(red("Please execute dotfiles.fetch"))
    run('cd %(dotfiles)s ; git pull' % locals())

    # Synchronize system
    cmd = 'rsync -avr --exclude ".git/" "%(dotfiles)s/%(src)s" "%(dst)s"' % locals()
    if use_sudo:
        sudo(cmd)
    else:
        run(cmd)
