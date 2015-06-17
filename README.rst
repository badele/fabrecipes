About
-----

Fabrecipes it's samples of Fabric and Fabtools scrips. In the future, the script will offer a auto install package. For example, Archlinux autoinstallation or a Emacs with autoconfigured plugins.

Installation
----------------------------

.. code-block:: console
	
	git clone https://github.com/badele/fabrecipes.git
	cd fabrecipes
	mkvirtualenv --no-site-packages -p /usr/bin/python2.7 fabtools
	pip install -r requirements.txt
	add2virtualenv YOUDIRECTORY_PROJECT/fabrecipes


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

	$ cd fabrecipes/archlinux/autoinstall
	$ fab -H root@hostname  computer.virtualbox autoinstall.install
	[ ..  reboot your system ]
	$ fab -H root@hostname computer.virtualbox autoinstall.configure
	$ fab -H username@hostname autoinstall.env_xorg_xfce_i3
	$ fab -H username@hostname autoinstall.env_xorg_misc

**Configure**: For preventive, in your first installation on your computer, you can execute fab -H username@hostname archlinux.autoinstall.env_xorg instead of fab -H username@hostname archlinux.autoinstall.env_xorg_xfce_i3. This you permit fix X Windows problem (driver, screen resolution). after you have fixed and uploaded fix in your dotfiles direcctory, you will can in future, call fab -H username@hostname archlinux.autoinstall.env_xorg_xfce_i3


And if in the next day, if you would like again synchronize your dotfiles, just execute

.. code-block:: console

	$ fab -H username@hostname computer.virtualbox autoinstall.sync_dotfiles:env_xorg_xfce_i3


For more informations about archlinux auto installation see https://github.com/badele/fabrecipes/blob/master/fabrecipes/archlinux/README.rst
