About
-----

This recipes provide a zfs tools, it can :
 - Autoinstall a zfs system into Archlinux
 - Prepare a LIVE(ex: work directely external USB drive) crypted ZFS pool
 - Make historical snapshot
 - Replicate snapshot in another BACKUP disk.

Installation
------------

Before use the ZFS, you must install a kernel and utils

.. code-block:: console

	$ fab install

Utilization
-----------

Create a crypted ZFS pool (LIVE and BACKUP)


.. code-block:: console

	$ fab init_crypted_zfs:/dev/sdx,1,LIVE
	$ fab init_crypted_zfs:/dev/sdy,1,BACKUP
