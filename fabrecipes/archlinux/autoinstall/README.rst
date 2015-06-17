About
-----

This recipe, autoinstall a Archlinux distribution (2015.05.01) from a computer file configuration. Detailled step autoinstallation
Installation:

* **Automatic installation**

  * Format partition and create filesystem
  * Create a **encrypted** /home
  * Install base system
  * Install boot system

* **Automatic configuration**

  * Set hostname
  * Add user account
  * Define keymap, locale, timezone
  * Configure yaourt package manager 
  * Check if env packages is installed

    * base requirement
        * zsh
        * wget,
        * netctl
        * dialog
        * yaourt
        * python2
        * ifplugd
        * net-tools
        * wpa_actiond
        * wpa_supplicant
    * base
        * mc
        * tmux
        * dnsutils
        * alsa-utils
        * pulseaudio
        * mc-solarized-git
        * dircolors-solarized-git
    * xorg
        * gksu
        * xterm
        * arandr
        * xdotool
        * xorg-xev
        * xorg-xrdb
        * xorg-xkill
        * xorg-xinit
        * xorg-xprop
        * xorg-server
        * xorg-server-utils
        * xf86-input-synaptics
    * xfce + i3
        * feh
        * exo
        * gvfs
        * i3-wm
        * dmenu
        * xfwm4
        * xfconf
        * thunar
        * i3lock
        * tumbler
        * gvfs-smb
        * i3status
        * ristretto
        * xautolock
        * xfdesktop
        * xfce4-mixer
        * xfce4-panel
        * rxvt-unicode
        * xfwm4-themes
        * thunar-volman
        * xfce4-session
        * xfce4-settings
        * xfce4-terminal
        * xfce4-appfinder
        * gtk2-xfce-engine
        * shimmer-wallpapers
        * xfce4-power-manager
        * xfce-theme-albatross
    * misc
        * vlc
        * slop
        * maim
        * openvpn
        * firefox
        * remmina
        * freerdp
        * keepassx
        * flashplugin
        * pavucontrol
        * sox



  * **python2** with all packages installed with **pip**

    * virtualenv
    * virtualenvwrapper

* **Bonus autoinstallation**
  
  * Install your environement
  * Dotfiles synchronisation
 

Utilization
-----------

Before use it, you must have a fabtools environement on other computer(see the home fabrecipes README.rst for fabtools installation)

**First step**

***Disk partition***
.. code-block:: console

    $ loadkeys fr
    $ cfdisk /dev/sda # partition in dos mode
    $ reboot

***Prepare SSH connexion from ISO install***

.. code-block:: console

    $ loadkeys fr
    $ passwd
    $ systemctl start sshd
    $ ip addr # show IP ISO install

**Second Step**

***Prepare network connection***

Boot on a new installation (no booting on installation CD-ROM)

.. code-block:: console

    $ loadkeys fr
    $ dhcpcd
    $ systemctl start sshd

***Lauch installation from another PC***

from another PC execute this two lines for automatic installation in ``root@hostname``

.. code-block:: console

    $ cd fabrecipes/archlinux
    $ fab -H root@hostname  computer.virtualbox autoinstall.install
    [ ..  reboot your system .. ]
    $ fab -H root@hostname computer.virtualbox autoinstall.configure
    $ fab -H username@hostname autoinstall.env_xorg_xfce_i3
    $ fab -H username@hostname autoinstall.env_xorg_misc

Well, you have now a fresh installation with a encrypted /home folder and XFCE + I3 environment (see the video sample https://youtu.be/Z_Q8vXKB6Ok )

Finalise the configuration

.. code-block:: console

    $ nano /etc/udev/rules.d/10-network.rules

And, if in the next day, you would like synchronize again your dotfiles, just execute

.. code-block:: console

    $ fab -H username@hostname computer.virtualbox autoinstall.sync_dotfiles:env_xorg_xfce_i3


Example
-------
Here a content of computer_sample

.. code-block:: python

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

