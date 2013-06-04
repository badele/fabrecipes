# Fabric
from fabric.api import settings, env, task, sudo
from fabric.utils import abort
from fabric.colors import red
from fabric.operations import prompt, reboot

# Fabtools
from fabtools.require import file as require_file
from fabtools.utils import run_as_root
from fabric.contrib.files import append, comment, sed
from fabtools.files import watch, is_dir, is_link

from fabtools import require
from fabtools import python
from fabtools import system
from fabtools import arch
from fabtools import disk

"""
   This script autoinstall a new Archlinux distribution
   use 3 partitions
     /dev/sda1[Linux]
     /dev/sda2[Swap]
     /dev/sda3[Linux]

   For use this script

     1) Prepare SSH connexion from ISO install
        $ loadkeys fr
        $ passwd
        $ systemctl start sshd
        $ ip addr # show IP ISO install

     2) Create a computer_name in the archlinux.py (see computer_sample)
     3) $ fab -f fabrecipes/archlinux/autoinstall.py -H root@host computer_name install
     4) ... Reboot on your new installation
     5) $ fab -f fabrecipes/archlinux/autoinstall.py -H root@host computer_name configure

   It does that in two step:

   1)
     - Verify if fabric script connected to ISO install
     - Verify if you have all required partitions types, if yes,
       it format all partitions and mount partition
     - Install base system
     - Install boot system
     - reboot your system

   2)
     - Set hostname
     - Set locale
     - Set keybord keymap
     - Set timezone
     - Check if you have internet connection, for install packages
     - Configure yaourt package manager
     - Instal minimal packages

"""


@task
def computer_sample():
    """
    Sample computer configuration
    """
    env.hostname = 'sample-computer'
    env.useraccount = 'badele'
    env.dotfiles = 'https://github.com/badele/dotfiles.git'
    env.locale = 'fr_FR.UTF-8'
    env.keymap = 'fr-pc'
    env.timezone_continent = 'Europe'
    env.timezone_city = 'City'
    env.xorg = ['virtualbox-guest-utils']
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
def install():
    """
    Install archlinux in a new computer

    Please select profil begin by computer_

    loadkeys fr
    passwd
    systemctl start sshd
    now, you can connect to new computer from SSH

    # == HDD configuration
    # prepare partition with same confiration from computer_

    """
    if not 'hostname' in env:
        abort("Please select profil computer")

    require_isoinstall()
    require_partition()
    mount_partitions()
    install_base()
    set_root_password()
    prepare_boot()
    reboot_system()


@task
def configure():
    """
    Configure archlinux fresh installation

    Please select profil begin by computer_

    loadkeys fr
    passwd
    dhcpcd
    pacman -S openssh
    systemctl start sshd
    # clean you .ssh/know_hosts
    """
    if not 'hostname' in env:
        abort("Please select profil computer")

    run_as_root('systemctl enable sshd')
    require.system.hostname(env.hostname)
    require.system.default_locale(env.locale)
    require_keymap(env.keymap)
    require_timezone(env.timezone_continent, env.timezone_city)
    require_internet()
    require_yaourt_configuration()
    require.users.user(env.useraccount, shell='/usr/bin/zsh')
    env_base()


@task
def env_base(direct=True):
    """
    Install base system
    """
    if 'pkgs' not in env:
        env.pkgs = []

    pkgs = [
        'zsh',
        'yaourt',
        'wget',
        'git',
        'rsync',
        'sudo',
        'net-tools',
        'python2'
    ]
    env.pkgs = list(set(env.pkgs + pkgs))
    if direct:
        install_packages()

    python.get_python_location()
    require.python.pip()


@task
def env_terminal(direct=True):
    """
    Install with terminal customization
    """
    env_base(False)
    pkgs = [
        'tmux',
        'zsh',
        'screenfetch',
        'rxvt-unicode',
        'terminus-font',
        'mc',
    ]
    env.pkgs = list(set(env.pkgs + pkgs))
    if direct:
        install_packages()


@task
def env_xorg_base(direct=True):
    """
    Install base Xorg system
    """
    env_terminal(False)
    pkgs = [
        'xf86-input-synaptics',
        'xorg-server',
        'xorg-xinit',
        'xorg-xev',
        'xorg-xprop',
        'xorg-xrdb',
        'xterm',
        'slim',
        'slim-themes',
        'gksu',
        'arandr',
        'xdotool',
    ]
    env.pkgs = list(set(env.pkgs + pkgs + env.xorg))
    if direct:
        install_packages()


@task
def env_xorg_i3(direct=True):
    """
    Install xorg with i3 feature
    """
    env_xorg_base(False)
    pkgs = [
        'i3-wm',
        'i3lock',
        'i3status',
        'dmenu',
        'xautolock',
    ]
    env.pkgs = list(set(env.pkgs + pkgs))
    if direct:
        install_packages()


@task
def env_xorg_light(direct=True):
    """
    Install i3 with lightweight software
    """
    env_xorg_i3(False)
    pkgs = [
        'spacefm',
        'cifs-utils',
        'gigolo',
        'zathura',
        'zathura-pdf-mupdf',
        'wicd',
        'wicd-gtk',
        'volumeicon',
        'parcellite',
        'feh',
    ]
    env.pkgs = list(set(env.pkgs + pkgs))
    if direct:
        install_packages()


@task
def env_xorg_misc(direct=True):
    """
    Full Xorg installation
    (Xorg + i3 + lighweight + misc software)
    """
    env_xorg_light(False)
    pkgs = [
        'alsa-utils',
        'chromium',
        'flashplugin',
        'remmina',
        'freerdp',
        'keepassx',
        'openvpn',
        'xchat',
    ]
    env.pkgs = list(set(env.pkgs + pkgs))
    if direct:
        install_packages()


@task
def sync_dotfiles(workspace):
    dst = '/home/%(useraccount)s/dotfiles' % env
    cloned = False

    # Clone if not exists
    if not is_dir(dst):
        cmd = 'cd ; git clone %(dotfiles)s' % env
        sudo(cmd, user=env.useraccount)
        cloned = True

    # Pull dotfiles project
    if not cloned:
        # Mise a jours des sources
        cmd = 'cd ~/dotfiles ; git pull'
        sudo(cmd, user=env.useraccount)

    # Synchronize system
    cmd = 'rsync -avr --exclude ".git/" %(dst)s/system/ /' % locals()
    run_as_root(cmd)

    # Synchronize user
    cmd = 'rsync -avr --exclude ".git/" --cvs-exclude %(dst)s/user/ ~/' % locals()
    sudo(cmd, user=env.useraccount)

    # Configure i3 with workspace
    if is_link('/home/%(useraccount)s/.i3/config' % env):
        sudo('rm ~/.i3/config', user=env.useraccount)
    cmd = 'ln -s ~/.i3/config_%(workspace)s ~/.i3/config' % locals()
    sudo(cmd, user=env.useraccount)

    # Configure ZSH
    if not is_dir('/home/%(useraccount)s/.oh-my-zsh' % env):
        cmd = 'cd ; git clone https://github.com/rkj/oh-my-zsh ~/.oh-my-zsh'  # Fix rkj theme problem

        sudo(cmd, user=env.useraccount)
    require.python.package('virtualenvwrapper')


def install_packages():
    """
    Install all packages in env.pkgs variable
    """
    require.arch.packages(env.pkgs)


def run_on_archroot(cmd):
    """
    chroot on the new installation
    """
    run_as_root('arch-chroot /mnt %s' % cmd)


def require_isoinstall():
    """
    check if run in the ISO installation
    """
    if system.get_hostname() != "archiso":
        abort("You seem not execute this script on iso install")


def require_partition():
    """
    Check if all partitions type exist and format
    """
    spart = {'Linux': 0x83, 'Swap': 0x82}
    p = disk.partitions()

    r = p[env.part['/boot']['device']] == spart['Linux']
    r = r and p[env.part['swap']['device']] == spart['Swap']
    r = r and p[env.part['lvm']['device']] == spart['Linux']

    if not r:
        abort("can't continue, not found require partitions")

    # Format partition
    r = prompt(red('Please Confirm you wan (re)-format with Y'))
    if r != "Y":
        abort("You do not want to continue :)")

    # disk.mkfs(env.part['/']['device'], env.part['/']['ftype'])

    # Prepare system partition
    disk.mkfs(env.part['/boot']['device'], env.part['/boot']['ftype'])
    disk.mkswap(env.part['swap']['device'])

    # Initialize lvm parition
    run_as_root('pvcreate -yff -Z y %s' % env.part['lvm']['device'])
    run_as_root('vgcreate -yff -Z y vg %s' % env.part['lvm']['device'])

    # Create partition
    run_as_root('lvcreate -n %s -L %s' %
                (env.part['/']['device'], env.part['/']['size']))
    run_as_root('lvcreate -n %s -L %s' %
                (env.part['/home']['device'], env.part['/home']['size']))

    # Format root on LVM
    disk.mkfs(env.part['/']['device'], env.part['/']['ftype'])

    # Format home on LVM
    print(red('Encrypt home partition, manual intervention needed'))
    run_as_root('cryptsetup luksFormat %s' % env.part['/home']['device'])

    print(red('Open home partition, manual intervention needed'))
    run_as_root('cryptsetup luksOpen %s home' % env.part['/home']['device'])
    disk.mkfs('/dev/mapper/home', env.part['/home']['ftype'])
    run_as_root('tune2fs -m 0 /dev/mapper/home')


def mount_partitions():
    """
    mount all paritions
    """
    disk.mount(env.part['/']['device'], "/mnt/")
    if not is_dir('/mnt/boot'):
        run_as_root('mkdir /mnt/boot')

    if not is_dir('/mnt/home'):
        run_as_root('mkdir /mnt/home')

    disk.mount(env.part['/boot']['device'], "/mnt/boot")
    disk.mount('/dev/mapper/home', "/mnt/home")
    disk.swapon(env.part['swap']['device'])


def install_base():
    """
    Install base system
    """
    run_as_root('pacstrap /mnt base base-devel syslinux openssh')
    run_as_root('genfstab -U -p /mnt >> /mnt/etc/fstab')


def set_root_password():
    print(red("Define Root password"))
    run_on_archroot('passwd')


def reboot_system():
    """
    Reboot system for the next step
    """
    print("Please wait and do the next step: ")
    print("""From you physical computer
# after reboot select "Boot existing OS"
loadkeys fr
dhcpcd
systemctl start sshd
""")
    print("fab -f fabrecipes/archlinux/autoinstall.py -H root@%s computer_sample configure" % env.host)
    reboot(1)



def require_keymap(keymap):
    """
    Check a keymap
    """
    conf = 'KEYMAP=%s' % keymap
    config_file = '/etc/vconsole.conf'
    require_file(config_file, conf, use_sudo=True)


def require_timezone(zone, city):
    """
    Check a timezone
    """
    config_file = '/etc/localtime'
    link = '/usr/share/zoneinfo/%(zone)s/%(city)s' % locals()
    if is_link(config_file):
        run_as_root('rm %(config_file)s' % locals())
    run_as_root('ln -s %(link)s %(config_file)s' % locals())
    run_as_root('hwclock --systohc --utc')


def prepare_boot():
    """
    Install boot
    """
    # Prepare mkinitcpio
    config_file = '/mnt/etc/mkinitcpio.conf'
    comment(config_file, '^HOOKS')
    with watch(config_file):
        append(config_file, 'HOOKS="base udev autodetect modconf block keyboard lvm2 encrypt filesystems fsck"')
    run_on_archroot('mkinitcpio -p linux')

    # Prepare syslinux
    config_file = '/mnt/boot/syslinux/syslinux.cfg'
    with watch(config_file):
        sed(config_file, 'root=/dev/sda3', 'root=/dev/vg/root')
    run_on_archroot('syslinux-install_update -iam')

    # Configure home encrypted mount
    config_file = '/mnt/etc/crypttab'
    with watch(config_file):
        append(config_file, 'home /dev/vg/home', 'root=/dev/vg/root')


def require_internet():
    """
    Check if they have a internet connexion
    """
    with settings(warn_only=True):
        res = run_as_root('ping -c1 -W1 8.8.8.8')
        if res.return_code == 1:
            abort("You must have internet to be continue")


def require_yaourt_configuration():
    """
    Add a yaourt configuration
    """
    config_file = '/etc/pacman.conf'

    with watch(config_file, use_sudo=True) as config:
        append(config_file, '[archlinuxfr]', use_sudo=True)
        append(config_file, 'Server = http://repo.archlinux.fr/%s' % env.arch, use_sudo=True)

    if config.changed:
        append(config_file, 'SigLevel = Optional', use_sudo=True)
        arch.update_index()
