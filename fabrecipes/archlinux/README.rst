About
-----

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
    
  * **python2** with all packages installed with **pip**

    * virtualenv
    * virtualenvwrapper

* **Bonus autoinstallation**
  
  * Install your environement
  * Dotfiles synchronisation
 

Utilization
-----------

Before use it, you must have a fabtools environement (see the home fabrecipes README.rst for fabtools installation)

**Prepare SSH connexion from ISO install**


.. code-block:: console

   $ loadkeys fr
   $ passwd
   $ systemctl start sshd
   $ ip addr # show IP ISO install

**Lauch installation from another PC**

from another PC execute this two lines for automatic installation in ``root@hostname``

.. code-block:: console

   $ fab -f autoinstall/archlinux.py -H root@hostname computer_sample install
   [ ..  reboot your system ]
   $ fab -f autoinstall/archlinux.py -H root@hostname computer_sample configure env_xorg_i3 sync_dotfiles:home
   
Well, you have now a fresh installation with a encrypted /home folder and i3 environment
