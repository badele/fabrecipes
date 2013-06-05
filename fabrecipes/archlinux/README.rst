Before use it, you must have a fabtools environement (see the home fabrecipes README.rst for fabtools installation)

This recipe, autoinstall a Archlinux distribution from a computer file configuration. Detailled step autoinstallation
Installation:
- Format partition and create filesystem
- Create a encrypted /home
- Install base system
- Install boot system

Cofiguration:
- Set hostname
- Add user account
- Define keymap, locale, timezone
- Configure yaourt package manager 
- Install base packages
        'zsh',
        'yaourt',
        'wget',
        'git',
        'rsync',
        'sudo',
        'net-tools',
        'python2'
