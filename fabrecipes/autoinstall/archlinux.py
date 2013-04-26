# Fabric
from fabric.api import settings, env, task
from fabric.utils import abort
from fabric.colors import red
from fabric.operations import prompt, reboot

# Fabtools
from fabtools.require import file as require_file
from fabric.contrib import files
from fabtools.utils import run_as_root
from fabric.contrib.files import append
from fabtools.files import watch, is_dir

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

   For use this script

     1) Create a computer_name in the archlinux.py (see computer_sample)
     2) execture fab -f autoinstall/archlinux/archlinux.py -H root@host computer_name install
     3) ... Reboot you new installation
     4) fab -f autoinstall/archlinux/archlinux.py -H root@host computer_name configure
"""


@task
def install():
    """
    Install archlinux in a new computer

    Please select profil begin by computer\_

    loadkeys fr
    passwd
    systemctl start sshd
    now, you can connect to new computer from SSH

    # == HDD configuration
    # prepare partition with same confiration from computer\_.env.part

    """
    if not 'hostname' in env:
        abort("Please select profil computer")

    require_isoinstall()
    require_partition()
    mount_partitions()
    install_base()
    require_install_boot()
    reboot_system()


@task
def configure():
    """
    Configure archlinux fresh installation

    Please select profil begin by computer\_

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


@task
def computer_sample():
    """
    Profile for HP Pavilion G Series
    """
    env.hostname = 'virtualbox'
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
    run_as_root('arch-chroot /mnt %s' % cmd)


def require_isoinstall():
    if system.get_hostname() != "archiso":
        abort("You seem not execute this script on iso install")


def require_partition():
    # Check if all partitions type exist
    spart = {'Linux': 83, 'Swap': 82}
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
    disk.mount(env.part['/']['device'], "/mnt/")
    if not is_dir('/mnt/boot'):
        run_as_root('mkdir /mnt/boot')

    disk.mount(env.part['/boot']['device'], "/mnt/boot")
    disk.swapon(env.part['swap']['device'])


def install_base():
    run_as_root('pacstrap /mnt base base-devel syslinux')
    run_as_root('genfstab -U -p /mnt >> /mnt/etc/fstab')


def reboot_system():
    print ("Please wait and do the next step: ")
    print ("""From you physical computer
loadkeys fr
passwd
dhcpcd
pacman -S openssh
systemctl start sshd
# clean you .ssh/know_hosts
""")
    print ("fab first_configuration:hostname=%s" % env.hostname)
    reboot(30)


def require_user():
    require.users.user('badele')


def require_keymap(keymap):
    conf = 'KEYMAP=%s' % keymap
    config_file = '/etc/vconsole.conf'
    require_file(config_file, conf, use_sudo=True)


def require_timezone(zone, city):
    config_file = '/etc/localtime'
    link = '/usr/share/zoneinfo/%(zone)s/%(city)s' % locals()
    if files.exists(config_file):
        run_as_root('rm %(config_file)s' % locals())
    run_as_root('ln -s %(link)s %(config_file)s' % locals())


def require_install_boot():
    run_on_archroot('mkinitcpio -p linux')
    run_on_archroot('syslinux-install_update -iam')


def require_internet():
    with settings(warn_only=True):
        res = run_as_root('ping -c1 -W1 8.8.8.8')
        if res.return_code == 1:
            abort("You must have internet to be continue")


def require_yaourt_configuration():
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
