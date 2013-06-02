About
-----

Fabrecipes it's samples of Fabric and Fabtools scrips. In the future, the script will offer a auto install package. For example, Archlinux autoinstallation or a Emacs with autoconfigured plugins.

Installation
----------------------------

.. code-block:: console
	
	git clone https://github.com/badele/fabrecipes.git
	cd fabrecipes
	mkvirtualenv --no-site-packages fabtools
	workon fabtools
	pip install -r requirements.txt


Example
-------


Example, you would like install automatically a new Archlinux. 

**Prepare SSH connexion from ISO install**


.. code-block:: console

	$ loadkeys fr
	$ passwd
	$ systemctl start sshd
	$ ip addr # show IP ISO install

and from another PC execute this two lines

.. code-block:: console

	$ fab -f autoinstall/archlinux.py -H root@hostname computer_sample install
	[ ..  reboot your system ]
	$ fab -f autoinstall/archlinux.py -H root@hostname computer_sample configure env_i3 sync_dotfiles
	

And if in the next day, you would like again synchronize your dotfiles, just execute

.. code-block:: console

	$ fab -f autoinstall/archlinux.py -H root@hostname sync_dotfiles


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
	    env.keymap = 'fr-pc'
	    env.timezone_continent = 'Europe'
	    env.timezone_city = 'City'
	    env.xorg = ['virtualbox-guest-utils']
	    env.arch = 'x86_64'
	    env.disk = '/dev/sda'
	    env.part = {
	        '/': {'device': '/dev/sda3', 'ptype': 'Linux', 'ftype': 'ext4'},
	        '/boot': {'device': '/dev/sda1', 'ptype': 'Linux', 'ftype': 'ext2'},
	        'swap': {'device': '/dev/sda2', 'ptype': 'Linux swap / Solaris', 'ftype': 'swap'},
	    }
