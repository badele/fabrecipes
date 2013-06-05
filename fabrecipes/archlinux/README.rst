About
-----

Before use it, you must have a fabtools environement (see the home fabrecipes README.rst for fabtools installation)

Utilization
------

This recipe, autoinstall a Archlinux distribution from a computer file configuration. Detailled step autoinstallation
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
  * Check if base packages is installed

    * zsh
    * yaourt
    * wget
    * git
    * rsync
    * sudo
    * net-tools
    * python2

* **Bonus autoinstallation**
  
  * Dotfiles synchronisation
  * Install your environement
