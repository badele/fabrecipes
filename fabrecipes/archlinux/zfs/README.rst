About
-----

i have multiple material failure with my computer (desktop and notebook) and after these incidents i am less productive.
For this reason, i have developed fabrecipes and especially the zfs module.
Now, i work directly on live USB disk. if i have a new material failure, i just need change the computer.

This recipes provide a zfs tools, it can :
 
- Autoinstall a zfs system into Archlinux
- Prepare a LIVE(ex: work directely external USB drive) crypted ZFS pool
- Make historical snapshot
- Replicate snapshot in another BACKUP pool.

Installation
------------

Before use the ZFS, you must install a kernel and utils

.. code-block:: console

    $ fab install

Preparation
-----------

**Create a crypted ZFS pool (LIVE and BACKUP)**


.. code-block:: console

    $ fab init_crypted_zfs:/dev/sdx,1,LIVE
    $ fab init_crypted_zfs:/dev/sdy,1,BACKUP


**Add a dataset in LIVE pool (example)**

.. code-block:: console

    $ zfs create documents
    $ zfs create projects
    $ zfs create others

Utilization
-----------

**Create snapshot into the LIVE ZFS pool**

.. code-block:: console

    $ fab bk_snaphots

**Replicate into the BACKUP ZFS pool**

.. code-block:: console

    $ fab bk_replicates
    

**Example snapshot result**

.. code-block:: console

    $ sudo zfs list -t snap

    LIVE/documents@2013-09-06_19:51            0      -   216M  -
    LIVE/documents@2013-09-06_19:52            0      -   216M  -
    LIVE/documents@2013-09-06_19:54            0      -   216M  -
    LIVE/documents@2013-09-06_19:55            0      -   216M  -
    LIVE/documents@2013-09-06_19:57         140K      -   216M  -
    LIVE/documents@2013-09-08_16:35            0      -   216M  -
    LIVE/documents@2013-09-08_17:11            0      -   216M  -
    LIVE/documents@2013-09-09_19:09         188K      -   216M  -
    LIVE/projects@2013-09-06_19:51          212K      -  1,76G  -
    LIVE/projects@2013-09-06_19:52          212K      -  1,76G  -
    LIVE/projects@2013-09-06_19:54          220K      -  1,76G  -
    LIVE/projects@2013-09-06_19:55          212K      -  1,76G  -
    LIVE/projects@2013-09-06_19:57          212K      -  1,76G  -
    LIVE/projects@2013-09-08_16:35          228K      -  1,76G  -
    LIVE/projects@2013-09-08_17:11          236K      -  1,76G  -
    LIVE/projects@2013-09-09_19:09          392K      -  1,76G  -
    LIVE/scripts@2013-09-06_19:51              0      -  1,85M  -
    LIVE/scripts@2013-09-06_19:52              0      -  1,85M  -
    LIVE/scripts@2013-09-06_19:54              0      -  1,85M  -
    LIVE/scripts@2013-09-06_19:55              0      -  1,85M  -
    LIVE/scripts@2013-09-06_19:57              0      -  1,85M  -
    LIVE/scripts@2013-09-08_16:35              0      -  1,85M  -
    LIVE/scripts@2013-09-08_17:11              0      -  1,85M  -
    LIVE/scripts@2013-09-09_19:09              0      -  1,85M  -
    BACKUP/documents@2013-09-06_19:51         1K      -   209M  -
    BACKUP/documents@2013-09-06_19:52         1K      -   209M  -
    BACKUP/documents@2013-09-06_19:54         1K      -   209M  -
    BACKUP/documents@2013-09-06_19:55         1K      -   209M  -
    BACKUP/documents@2013-09-06_19:57      58,5K      -   209M  -
    BACKUP/documents@2013-09-08_16:35         1K      -   209M  -
    BACKUP/documents@2013-09-08_17:11         1K      -   209M  -
    BACKUP/documents@2013-09-09_19:09        84K      -   209M  -
    BACKUP/projects@2013-09-06_19:51        105K      -  1,69G  -
    BACKUP/projects@2013-09-06_19:52        105K      -  1,69G  -
    BACKUP/projects@2013-09-06_19:54        112K      -  1,69G  -
    BACKUP/projects@2013-09-06_19:55        105K      -  1,69G  -
    BACKUP/projects@2013-09-06_19:57        105K      -  1,69G  -
    BACKUP/projects@2013-09-08_16:35        128K      -  1,69G  -
    BACKUP/projects@2013-09-08_17:11        130K      -  1,69G  -
    BACKUP/projects@2013-09-09_19:09        137K      -  1,69G  -
    BACKUP/scripts@2013-09-06_19:51           1K      -  1,58M  -
    BACKUP/scripts@2013-09-06_19:52           1K      -  1,58M  -
    BACKUP/scripts@2013-09-06_19:54           1K      -  1,58M  -
    BACKUP/scripts@2013-09-06_19:55           1K      -  1,58M  -
    BACKUP/scripts@2013-09-06_19:57           1K      -  1,58M  -
    BACKUP/scripts@2013-09-08_16:35           1K      -  1,58M  -
    BACKUP/scripts@2013-09-08_17:11           1K      -  1,58M  -
    BACKUP/scripts@2013-09-09_19:09           1K      -  1,58M  -

