import inspect
from re import escape

# Fabric
from fabric.api import settings, env, task, sudo, run
from fabric.utils import abort
from fabric.colors import red
from fabric.operations import prompt, reboot
from fabric.contrib.files import append, comment, uncomment, sed

# Fabtools
from fabtools.require import file as require_file
from fabtools.utils import run_as_root
from fabtools.files import watch, is_dir, is_link
from fabtools import arch
from fabtools import disk
from fabtools import python
from fabtools import require
from fabtools import systemd
from fabtools import system
from fabtools import user


# Fabrecipes
from fabrecipes.commons import dotfiles
from fabrecipes import computer

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

    #run_as_root('systemctl enable sshd')
    require.system.hostname(env.hostname)
    require_locale(env.locale, env.charset)
    require_keymap(env.keymap)
    require_timezone(env.timezone_continent, env.timezone_city)
    require_internet()
    require_yaourt_configuration()
    require.users.user(env.useraccount)
    require.users.sudoer(env.useraccount, passwd=True)


@task
def env_base(direct=True, sync_dotfiles='fabrecipes'):
    """
    Install base system
    """
    pkgs = [
        'zsh',
        'yaourt',
        'python2',
        'tmux',
        'net-tools',
        'wget',
        'wicd',
    ]

    # Check if a custom package for computer
    env_section = inspect.stack()[0][3]
    if 'pkgs' in env and env_section in env.pkgs:
        pkgs = list(set(pkgs + env.pkgs[env_section]))

    # Install required packages
    require.arch.packages(pkgs)

    # Install oh-my-zsh
    ohmyzsh = '$HOME/.oh-my-zsh'
    if not is_dir(ohmyzsh):
        run(
            'git clone git://github.com/robbyrussell/oh-my-zsh.git %(ohmyzsh)s'
            % locals()
        )

    # Set default ZSH shell for user
    if user.exists(env.useraccount):
        user.modify(env.useraccount, shell='/usr/bin/zsh')

    # Synchronize user dotfiles
    sync_dotfiles = 'fabrecipes/autoinstall/%(env_section)s' % locals()
    dotfiles.sync('%(sync_dotfiles)s/user/' % locals(), '$HOME/')
    dotfiles.sync('%(sync_dotfiles)s/sys/' % locals(), '/', use_sudo='true')

    # Configure base
    configure_base()


@task
def env_xorg():
    """
    Install base Xorg system
    """
    pkgs = [
        'xorg-server',
        'xorg-xinit',
        'xorg-xev',
        'xorg-xprop',
        'xorg-xrdb',
        'xorg-xkill',
        'xterm',
        'gksu',
        'arandr',
        'xdotool',
        'xorg-server-utils',
        'alsa-utils',
        'wicd-gtk',

    ]
    # Check if a custom package for computer
    env_section = inspect.stack()[0][3]
    if 'pkgs' in env and env_section in env.pkgs:
        pkgs = list(set(pkgs + env.pkgs[env_section]))

    # Install required packages
    env_base()
    require.arch.packages(pkgs)

    # Synchronize user dotfiles
    sync_dotfiles = 'fabrecipes/autoinstall/%(env_section)s' % locals()
    dotfiles.sync('%(sync_dotfiles)s/user/' % locals(), '$HOME/')
    dotfiles.sync('%(sync_dotfiles)s/sys/' % locals(), '/', use_sudo='true')

    # Configure_xorg
    configure_xorg()


@task
def env_xorg_xfce_i3():
    """
    Install xorg xfce feature
    """

    # if not arch.is_installed('xfce4-power-manager') and \
    #    not arch.is_installed('xfce4-wavelan-plugin'):
    pkgs = [
        # XFCE
        'exo',
        'garcon',
        'gtk2-xfce-engine',
        'gtk3-xfce-engine',
        'thunar',
        'thunar-volman',
        'tumbler',
        'xfce4-appfinder',
        'xfce4-mixer',
        'xfce4-panel',
        'xfce4-power-manager',
        'xfce4-session',
        'xfce4-settings',
        'xfce4-terminal',
        'xfconf',
        'xfdesktop',
        'xfwm4',
        'xfwm4-themes',
        #'xfce4-goodies',
        #'xfce-theme-manager',
        'xfce-theme-albatross',
        #'gtk-engine-unico',
        'elementary-xfce-icons',
        'shimmer-wallpapers',
        #
        # I3
        'i3-wm',
        'i3status',
        'dmenu',
        'i3lock',
        'xautolock',
        #
        # Commons
        'gvfs',
        'gvfs-smb',
    ]
    # Check if a custom package for computer
    env_section = inspect.stack()[0][3]
    if 'pkgs' in env and env_section in env.pkgs:
        pkgs = list(set(pkgs + env.pkgs[env_section]))

    # Install required packages
    env_xorg()
    require.arch.packages(pkgs)

    # Synchronize user dotfiles
    sync_dotfiles = 'fabrecipes/autoinstall/%(env_section)s' % locals()
    dotfiles.sync('%(sync_dotfiles)s/user/' % locals(), '$HOME/')
    dotfiles.sync('%(sync_dotfiles)s/sys/' % locals(), '/', use_sudo='true')


    configure_xfce_i3()


@task
def env_xorg_misc(direct=True):
    """
    Full Xorg installation
    (Xorg + i3 + lighweight + misc software)
    """
    env_xorg_base(False)
    pkgs = [
        'firefox',
        'flashplugin',
        'remmina',
        'freerdp',
        'keepassx',
        'openvpn',
        'xchat',
    ]
    env.pkgs = list(set(env.pkgs + pkgs))
    if direct:
        require.arch.packages(env.pkgs)
        configure_base()
        configure_xorg()
        configure_terminal()


def configure_base():
    # Configure python environement
    use_python = 'python2.7'
    require.python.pip(use_python=use_python)
    require.python.package('virtualenv', use_python=use_python, use_sudo=True)
    require.python.package('virtualenvwrapper', use_python=use_python, use_sudo=True)

    # Active service
    systemd.enable('dhcpcd')
    systemd.enable('sshd')
    systemd.enable('wicd')


def configure_xorg():
    # Xorg keymap
    keymap_file = '/etc/X11/xorg.conf.d/10-keyboard-layout.conf'
    append(keymap_file, 'Section "InputClass"', use_sudo=True)
    append(keymap_file, '  Identifier         "Keyboard Layout"', use_sudo=True)
    append(keymap_file, '  MatchIsKeyboard    "yes"', use_sudo=True)
    append(keymap_file, '  MatchDevicePath    "/dev/input/event*"', use_sudo=True)
    append(keymap_file, '  Option             "XkbLayout"  "%s"' %
           env.xkblayout, use_sudo=True)
    append(keymap_file, '  Option             "XkbVariant" "%s"' %
           env.xkbvariant, use_sudo=True)
    append(keymap_file, 'EndSection', use_sudo=True)


def configure_xfce_i3():
    hostname = env.hostname
    username = env.useraccount

    # Init XFCE sessions
    prefix = '$HOME/.cache/sessions/xfce4-session'
    src = '%(prefix)s-HOSTNAME:0' % locals()
    session = '%(prefix)s-%(hostname)s:0' % locals()
    run('mv "%(src)s" "%(session)s"' % locals())
    sed(session, escape('{{USERNAME}}'), username)
    sed(session, escape('{{HOSTNAME}}'), hostname)

    # Autologin
    autologin = '/etc/systemd/system/getty@tty1.service.d/autologin.conf'
    sed(autologin, escape('{{USERNAME}}'), username, use_sudo=True)


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
    run_as_root('pacstrap /mnt base base-devel syslinux openssh git rsync sudo')
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


def require_locale(locale, charset):
    """
    Set locale
    """
    config_file = '/etc/locale.gen'
    uncomment(config_file, '%s %s' % (locale, charset))
    require.system.default_locale(locale)
    run_as_root('locale-gen')


def require_keymap(keymap):
    """
    Check a keymap
    """
    conf = 'KEYMAP=%s' % keymap
    config_file = '/etc/vconsole.conf'
    require_file(config_file, conf)


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

    with watch(config_file) as config:
        append(config_file, '[archlinuxfr]')
        append(config_file, 'SigLevel = Never')
        append(config_file, 'Server = http://repo.archlinux.fr/%s' % env.arch)

        if env.arch == 'x86_64':
            append(config_file, '[multilib]')
            append(config_file, 'Include = /etc/pacman.d/mirrorlist # multilib')

    if config.changed:
        append(config_file, 'SigLevel = Optional')
        arch.update_index()
