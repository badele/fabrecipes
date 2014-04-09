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

   $ cd fabrecipes/archlinux/autoinstall
   $ fab -H root@hostname  computer.virtualbox archlinux.autoinstall.install
   [ ..  reboot your system ]
   $ fab -H root@hostname computer.virtualbox archlinux.autoinstall.configure
   $ fab -H username@hostname archlinux.autoinstall.env_xorg_xfce_i3
   $ fab -H username@hostname archlinux.autoinstall.env_xorg_misc
   
Well, you have now a fresh installation with a encrypted /home folder and i3 environment

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

