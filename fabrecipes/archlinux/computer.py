# Fabric
from fabric.api import env, task


@task
def computer_sample():
    """
    Sample computer configuration
    """
    env.hostname = 'sample-computer'
    env.useraccount = 'badele'
    env.dotfiles = 'https://github.com/badele/dotfiles.git'
    env.locale = 'fr_FR.UTF-8'
    env.charset = 'UTF-8'
    env.keymap = 'fr-pc'
    env.xkblayout = 'fr'
    env.xkbvariant = 'latin9'
    env.timezone_continent = 'Europe'
    env.timezone_city = 'City'
    env.pkgs = ['virtualbox-guest-utils']
    env.arch = 'x86_64'
    env.disk = '/dev/sda'
    env.part = {
        'lvm': {'device': '/dev/sda3', 'ptype': 'Linux'},
        '/': {
            'device': '/dev/vg/root',
            'ptype': 'Linux',
            'ftype': 'ext4',
            'size': '4g'
        },
        '/home': {
            'device': '/dev/vg/home',
            'ptype': 'Linux',
            'ftype': 'ext4',
            'size': '1.5g'
        },
        '/boot': {
            'device': '/dev/sda1',
            'ptype': 'Linux',
            'ftype': 'ext2'
        },
        'swap': {
            'device': '/dev/sda2',
            'ptype': 'Linux swap / Solaris',
            'ftype': 'swap'
        },
    }


@task
def jsl_acerone():
    """
    Acer Aspire One netbook
    installed on xx minutes
    fab -f autoinstall/archlinux.py -H root@hostname computer_sample install
    fab -f autoinstall/archlinux.py -H root@hostname computer_sample configure env_i3 sync_dotfiles
    """
    env.hostname = 'acerone'
    env.useraccount = 'badele'
    env.dotfiles = 'https://github.com/badele/dotfiles.git'
    env.locale = 'fr_FR.UTF-8'
    env.charset = 'UTF-8'
    env.keymap = 'fr-pc'
    env.xkblayout = 'fr'
    env.xkbvariant = 'latin9'
    env.timezone_continent = 'Europe'
    env.timezone_city = 'City'
    env.pkgs = ['xf86-video-intel', 'xf86-input-synaptics']
    env.arch = 'x86_64'
    env.disk = '/dev/sda'
    env.part = {
        'lvm': {'device': '/dev/sda3', 'ptype': 'Linux'},
        '/': {
            'device': '/dev/vg/root',
            'ptype': 'Linux',
            'ftype': 'ext4',
            'size': '30g'
        },
        '/home': {
            'device': '/dev/vg/home',
            'ptype': 'Linux',
            'ftype': 'ext4',
            'size': '100g'
        },
        '/boot': {
            'device': '/dev/sda1',
            'ptype': 'Linux',
            'ftype': 'ext2'
        },
        'swap': {
            'device': '/dev/sda2',
            'ptype': 'Linux swap / Solaris',
            'ftype': 'swap'
        },
    }
