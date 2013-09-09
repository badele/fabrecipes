# Fabric
from fabric.api import env, task, sudo, run
from fabric.utils import abort

# Fabtools
from fabtools.files import is_dir
from fabric.colors import red


def fetch(git=''):
    """
    Clone dotfiles project to ~/dotfiles
    """
    cloned = False
    if 'dotfiles' in env:
        git = env.dotfiles

    # Check project is already cloned
    if git != '' and not is_dir('/home/%(user)s/dotfiles' % env):
        cmd = 'cd ; git clone %(git)s' % locals()
        run(cmd)
        cloned = True

    # update locally dotfiles
    dotfiles = '/home/%(user)s/dotfiles' % env
    if not cloned and not is_dir(dotfiles):
        abort(red("Please execute dotfiles.fetch"))

    cmd = 'cd %(dotfiles)s ; git pull' % locals()
    run(cmd)


def sync(src, dst, use_sudo='false'):
    """
    Copy file from dotfiles dot dst
    """
    use_sudo = use_sudo.lower() == 'true'

    # Update dotfiles
    fetch()

    # Synchronize system
    dotfiles = '/home/%(user)s/dotfiles' % env
    env_dotfiles = '%(dotfiles)s/%(src)s' % locals()
    if is_dir(env_dotfiles):
        cmd = 'rsync -avr --exclude ".git/" "%(env_dotfiles)s" "%(dst)s"' % locals()
        if use_sudo:
            sudo(cmd)
        else:
            run(cmd)
