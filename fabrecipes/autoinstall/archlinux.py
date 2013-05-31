# Fabric
from fabric.api import settings, env, task
from fabric.utils import abort
from fabric.colors import red
from fabric.operations import prompt, reboot

# Fabtools
from fabtools.require import file as require_file
from fabtools.utils import run_as_root
from fabric.contrib.files import append
from fabtools.files import watch, is_dir, is_link

from fabtools import require
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
     3) $ fab -f fabrecipes/autoinstall/archlinux.py -H root@host computer_name install
     4) ... Reboot on your new installation
     5) $ fab -f fabrecipes/autoinstall/archlinux.py -H root@host computer_name configure

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
    require_install_boot()
    set_root_password()
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

    require.system.hostname(env.hostname)
    require.system.default_locale(env.locale)
    require_keymap(env.keymap)
    require_timezone(env.timezone_continent, env.timezone_city)
    require_internet()
    require_yaourt_configuration()
    require_minimal_packages()
    require.users.user(env.useraccount)


@task
def computer_sample():
    """
    Profile for HP Pavilion G Series
    """
    env.hostname = 'virtualbox'
    env.useraccount = 'badele'
    env.locale = 'fr_FR.UTF-8'
    env.keymap = 'fr-pc'
    env.timezone_continent = 'Europe'
    env.timezone_city = 'City'
    env.arch = 'x86_64'
    env.disk = '/dev/sda'
    env.part = {
        '/': {'device': '/dev/sda3', 'ptype': 'Linux', 'ftype': 'ext4'},
        '/boot': {'device': '/dev/sda1', 'ptype': 'Linux', 'ftype': 'ext2'},
        'swap': {'device': '/dev/sda2', 'ptype': 'Linux swap / Solaris', 'ftype': 'swap'},
    }


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
    r = r and p[env.part['/']['device']] == spart['Linux']

    if not r:
        abort("can't continue, not found require partitions")

    # Format partition
    r = prompt(red('Please Confirm you wan (re)-format with Y'))
    if r != "Y":
        abort("You do not want to continue :)")

    disk.mkfs(env.part['/']['device'], env.part['/']['ftype'])
    disk.mkfs(env.part['/boot']['device'], env.part['/boot']['ftype'])
    disk.mkswap(env.part['swap']['device'])


def mount_partitions():
    """
    mount all paritions
    """
    disk.mount(env.part['/']['device'], "/mnt/")
    if not is_dir('/mnt/boot'):
        run_as_root('mkdir /mnt/boot')

    disk.mount(env.part['/boot']['device'], "/mnt/boot")
    disk.swapon(env.part['swap']['device'])


def install_base():
    """
    Install base system
    """
    run_as_root('pacstrap /mnt base base-devel syslinux openssh')
    run_as_root('genfstab -U -p /mnt >> /mnt/etc/fstab')


def set_root_password():
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
    print("fab -f fabrecipes/autoinstall/archlinux.py -H root@%s computer_sample configure" % env.host)
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


def require_install_boot():
    """
    Install boot
    """
    run_on_archroot('mkinitcpio -p linux')
    run_on_archroot('syslinux-install_update -iam')


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


def require_minimal_packages():
    require.arch.packages([
        'yaourt',
        'wget',
        'git',
        'rsync',
        'sudo',
        'net-tools',
    ])
