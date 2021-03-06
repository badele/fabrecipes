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
        'env_xorg': [
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
            'size': '10g'
        },
        '/home': {
            'device': '/dev/vg/home',
            'ptype': 'Linux',
            'ftype': 'ext4',
            'size': '5g'
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
def lenovo450():
    """
    Lenovo 450s netbook
    installed on 30 minutes (15 Minutes + 1 minutes + 15 Minutes)
    $ cd fabrecipes/archlinux
    $ fab -H root@hostname computer.lenovo450 autoinstall.install
    $ fab -H root@hostname computer.lenovo450 archlinux.autoinstall.configure
    $ fab -H username@hostname computer.lenovo450 env_xorg_xfce_i3
    """
    env.hostname = 'lenovo450'
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
    env.timezone_city = 'Paris'
    env.pkgs = [
        'xf86-video-intel',
        'xf86-input-synaptics',
        'xf86-video-modesetting',
    ]
    env.arch = 'x86_64'
    env.disk = '/dev/sda'
    env.part = {
        'lvm': {'device': '/dev/sda3', 'ptype': 'Linux'},
        '/': {
            'device': '/dev/vg/root',
            'ptype': 'Linux',
            'ftype': 'ext4',
            'size': '50g'
        },
        '/home': {
            'device': '/dev/vg/home',
            'ptype': 'Linux',
            'ftype': 'ext4',
            'size': '200g'
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
def samsungn150():
    """
    Samsung n150 netbook
    installed on 30 minutes (15 Minutes + 1 minutes + 15 Minutes)
    $ cd fabrecipes/archlinux/autoinstall
    $ fab -H root@hostname computer.samsungn150 install
    $ fab -H root@hostname computer.virtualbox archlinux.autoinstall.configure
    $ fab -H username@hostname computer.samsungn150 env_xorg_xfce_i3
    """
    env.hostname = 'samsungn150'
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
    env.arch = 'x86_64'
    env.disk = '/dev/sda'
    env.part = {
        'lvm': {'device': '/dev/sda3', 'ptype': 'Linux'},
        '/': {
            'device': '/dev/vg/root',
            'ptype': 'Linux',
            'ftype': 'ext4',
            'size': '10g'
        },
        '/home': {
            'device': '/dev/vg/home',
            'ptype': 'Linux',
            'ftype': 'ext4',
            'size': '5g'
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
            'xfce4-whiskermenu-plugin',
            'galculator',
            'libreoffice-base',
            'libreoffice-calc',
            'libreoffice-draw',
            'libreoffice-impress',
            'libreoffice-math',
            'libreoffice-writer',
            'libreoffice-fr',
            'evince2-light',
            'ttf-ms-fonts',
            'flashplugin',
            'vlc',
            'freerdp',
            'remmina',
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
        ],
        'env_xorg': [
            'xf86-video-ati',
            'xfce4-sensors-plugin',
            'xfce4-whiskermenu-plugin',
            'galculator',
            'libreoffice-base',
            'libreoffice-calc',
            'libreoffice-draw',
            'libreoffice-impress',
            'libreoffice-math',
            'libreoffice-writer',
            'libreoffice-fr',
            'evince2-light',
            'ttf-ms-fonts',
            'flashplugin',
            'vlc',
            'freerdp',
            'remmina',
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
            'size': '20g'
        },
        '/home': {
            'device': '/dev/vg/home',
            'ptype': 'Linux',
            'ftype': 'ext4',
            'size': '90g'
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
def dell_latitude():
    """
    Dell Latitude
    installed on xx minutes
    cd fabrecipes/archlinux/autoinstall
    fab -H root@hostname computer.dell_latitude install
    fab -H root@hostname computer.dell_latitude configure env_xorg_i3 env_xorg_xfce
    """
    env.hostname = 'dell'
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
            'pulseaudio',
        ],
        'env_xorg': [
            'xf86-video-intel',
            'xfce4-sensors-plugin',
            'xfce4-whiskermenu-plugin',
            'galculator',
            'libreoffice-base',
            'libreoffice-calc',
            'libreoffice-draw',
            'libreoffice-impress',
            'libreoffice-math',
            'libreoffice-writer',
            'libreoffice-fr',
            'evince2-light',
            'ttf-ms-fonts',
            'flashplugin',
            'vlc',
            'freerdp',
            'remmina',
        ]
    }
    env.arch = 'x86_64'
    env.disk = '/dev/sda'
    env.part = {
        'lvm': {'device': '/dev/sda7', 'ptype': 'Linux'},
        '/': {
            'device': '/dev/vg/root',
            'ptype': 'Linux',
            'ftype': 'ext4',
            'size': '20g'
        },
        '/home': {
            'device': '/dev/vg/home',
            'ptype': 'Linux',
            'ftype': 'ext4',
            'size': '270g'
        },
        '/boot': {
            'device': '/dev/sda6',
            'ptype': 'Linux',
            'ftype': 'ext2'
        },
        'swap': {
            'device': '/dev/sda5',
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
