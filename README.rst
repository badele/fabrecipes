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


A summaries command list

.. code-block:: console

    $ fab -l                                                                                                                                                                                                                  !10019
    Available commands:

        capabilities                                Test capabilities functions in new distrition
        archlinux.autoinstall.configure             Configure archlinux fresh installation
        archlinux.autoinstall.env_base              Install base system
        archlinux.autoinstall.env_base_requirement  Install requirement base system
        archlinux.autoinstall.env_xorg              Install base Xorg system
        archlinux.autoinstall.env_xorg_misc         Full Xorg installation
        archlinux.autoinstall.env_xorg_xfce_i3      Install Xorg Xfce + I3 feature
        archlinux.autoinstall.install               Install archlinux in a new computer
        archlinux.autoinstall.sync_dotfiles         Synchronize the computer configuration from a dotfiles project
        archlinux.emacs.install_p2k                 Install emacs with some features in python 2.7 environement
        archlinux.pelican.install                   Install a pelican in python2 virtualenv
        archlinux.rstblog.install                   Install a rstblog in python2 virtualenv
        archlinux.virtualbox.install                Install virtualbox and use dkms virtual host modules
        archlinux.wine.install                      Install wine with customization
        archlinux.zfs.bk_replicates                 Replicate snapshot to another pool (default: BACKUP)
        archlinux.zfs.bk_snaprep                    Make a snapshots and replicates in the same time
        archlinux.zfs.bk_snapshots                  Create a today snapshot for the pool (default: LIVE)
        archlinux.zfs.init_crypted_zfs              Prepare a crypted ZFS disk
        archlinux.zfs.install                       Install zfs system (kernel + utils) from archzfs (demizerone repository)
        buildroot.bestsets.install                  Install bestset script from open-console
        computer.acer_inspireone                    Acer Aspire One netbook
        computer.dell_latitude                      Dell Latitude
        computer.hp_pavilion_g7                     HP Pavilion g7 Notebook PC
        computer.jsl_acer_inspireone_fix            Fix for Acer Aspire One netbook
        computer.lenovo450                          Lenovo 450s netbook
        computer.samsungn150                        Samsung n150 netbook
        computer.vaio_vgn_ns21s                     Sony Vaio VGN-NS21S netbook
        computer.virtualbox                         Sample computer configuration
        debian.docker.install                       Before use it, must do
        debian.docker.require_docker                Install a docker core
        debian.graphite.install                     Install graphite stack
        debian.hosting.addRootFlask                 Add a flask webserver
        debian.hosting.addWebserver                 Add a virtual webserver
        debian.hosting.install                      Prepare nginx hosting server
        debian.proxmox.recreate_pvedata             Recreate the pve-data with the defined size
        debian.seafile.install                      Seafile installation from the official documentation
        ubuntu.salt.master                          Install salt-master


For more informations about archlinux auto installation see https://github.com/badele/fabrecipes/blob/master/fabrecipes/archlinux/README.rst
