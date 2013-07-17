# Fabric
from fabric.api import settings, env, task, sudo
from fabric.utils import abort
from fabric.colors import red
from fabric.operations import prompt, reboot

# Fabtools
from fabtools.require import file as require_file
from fabtools.utils import run_as_root
from fabric.contrib.files import append, comment, uncomment, sed
from fabtools.files import watch, is_dir, is_link


@task
def virtualbox():
    """
    Sample computer configuration
    """
    env.hostname = 'sample-computer'
    env.useraccount = 'badele'
    env.dotfiles = 'https://github.com/badele/dotfiles.git'
    env.locale = 'fr_FR.UTF-8'
    env.charset = 'UTF-8'
    env.keymap = 'fr-pc'
    env.xsessions = 'xfce, i3'
    env.xautologin = 'yes'
    env.xkblayout = 'fr'
    env.xkbvariant = 'latin9'
    env.timezone_continent = 'Europe'
    env.timezone_city = 'City'
    env.pkgs = {
        'env_org': [
            'virtualbox-guest-utils',
            'xf86-video-vesa',
        ]
    }
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
def acer_inspireone():
    """
    Acer Aspire One netbook
    installed on xx minutes
    cd fabrecipes/archlinux/autoinstall
    fab -H root@hostname computer.acer_inspireone install
    fab -H root@hostname computer.acer_inspireone configure env_xorg_i3 env_xorg_xfce
    """
    env.hostname = 'acerone'
    env.useraccount = 'badele'
    env.dotfiles = 'https://github.com/badele/dotfiles.git'
    env.locale = 'fr_FR.UTF-8'
    env.charset = 'UTF-8'
    env.keymap = 'fr-pc'
    env.xsessions = 'xfce, i3'
    env.xautologin = 'yes'
    env.xkblayout = 'fr'
    env.xkbvariant = 'latin9'
    env.timezone_continent = 'Europe'
    env.timezone_city = 'City'
    env.pkgs = [
        'xf86-video-intel',
        'xf86-input-synaptics',
        'xf86-video-modesetting',
    ]
    env.arch = 'i686'
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


@task
def vaio_vgn_ns21s():
    """
    Sony Vaio VGN-NS21S netbook
    installed on xx minutes
    cd fabrecipes/archlinux/autoinstall
    fab -H root@hostname computer.vaio_vgn_ns21s install
    fab -H root@hostname computer.vgn_ns21s configure env_xorg_i3 env_xorg_xfce
    """
    env.hostname = 'vaio'
    env.useraccount = 'badele'
    env.dotfiles = 'https://github.com/badele/dotfiles.git'
    env.locale = 'fr_FR.UTF-8'
    env.charset = 'UTF-8'
    env.keymap = 'fr-pc'
    env.xsessions = 'xfce, i3'
    env.xautologin = 'yes'
    env.xkblayout = 'fr'
    env.xkbvariant = 'latin9'
    env.timezone_continent = 'Europe'
    env.timezone_city = 'City'
    env.pkgs = {
        'env_base': [
            'lm_sensors',
            'dnsutils',
        ],
        'env_xorg': [
            'xf86-video-ati',
            'xfce4-sensors-plugin',
            'libreoffice-base',
            'libreoffice-calc',
            'libreoffice-draw',
            'libreoffice-impress',
            'libreoffice-math',
            'libreoffice-writer',
            'libreoffice-fr',
            'epdfview',
            'ttf-ms-fonts',
        ]
    }
    env.arch = 'x86_64'
    env.disk = '/dev/sda'
    env.part = {
        'lvm': {'device': '/dev/sda4', 'ptype': 'Linux'},
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
            'size': '180g'
        },
        '/boot': {
            'device': '/dev/sda2',
            'ptype': 'Linux',
            'ftype': 'ext2'
        },
        'swap': {
            'device': '/dev/sda3',
            'ptype': 'Linux swap / Solaris',
            'ftype': 'swap'
        },
    }


def hp_pavilion_g7():
    """
    HP Pavilion g7 Notebook PC
    installed on xx minutes
    cd fabrecipes/archlinux/autoinstall
    fab -H root@hostname computer.hp_pavilion_g7 install
    fab -H root@hostname computer.hp_pavilion_g7 configure env_xorg_i3 env_xorg_xfce
    """
    env.hostname = 'hp2012'
    env.useraccount = 'badele'
    env.dotfiles = 'https://github.com/badele/dotfiles.git'
    env.locale = 'fr_FR.UTF-8'
    env.charset = 'UTF-8'
    env.keymap = 'fr-pc'
    env.xsessions = 'xfce, i3'
    env.xautologin = 'yes'
    env.xkblayout = 'fr'
    env.xkbvariant = 'latin9'
    env.timezone_continent = 'Europe'
    env.timezone_city = 'City'
    env.pkgs = {
        'env_base': [
            'lm_sensors',
            'dnsutils',
        ],
        'env_xorg': [
            'xf86-video-ati',
            'xfce4-sensors-plugin'
            'libreoffice-base',
            'libreoffice-calc',
            'libreoffice-draw',
            'libreoffice-impress',
            'libreoffice-math',
            'libreoffice-writer',
            'libreoffice-fr',
            'epdfview',
            'ttf-ms-fonts',
        ]
    }
    env.arch = 'x86_64'
    env.disk = '/dev/sda'
    env.part = {
        'lvm': {'device': '/dev/sda4', 'ptype': 'Linux'},
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
            'size': '180g'
        },
        '/boot': {
            'device': '/dev/sda2',
            'ptype': 'Linux',
            'ftype': 'ext2'
        },
        'swap': {
            'device': '/dev/sda3',
            'ptype': 'Linux swap / Solaris',
            'ftype': 'swap'
        },
    }


@task
def jsl_acer_inspireone_fix():
    """
    Fix for Acer Aspire One netbook
    - set xorg modesetting
    - disable numlock in notebook
    """
    xorgconf = '/etc/X11/xorg.conf.d/20-gpudriver.conf'
    if not is_dir(xorgconf):
        append(xorgconf, 'Section "Device"')
        append(xorgconf, '  Identifier "gma500_gfx"')
        append(xorgconf, '  Driver     "modesetting"')
        append(xorgconf, '  Option     "SWCursor"       "ON"')
        append(xorgconf, 'EndSection')

    # Configure slim
    slim_file = '/etc/slim.conf'
    comment(slim_file, '^numlock.*')
