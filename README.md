About
=====

Fabrecipes it's samples of Fabric and Fabtools scrips

Example
========

Example, you would like install automatically a new Archlinux, you have must just call this two line

``` console
   $ fab -f autoinstall/archlinux.py -H root@hostname computer_sample install 
   [ .. reboot your system ]
   $ fab -f autoinstall/archlinux.py -H root@hostname computer_sample configure 
```

Here a content of computer_sample

``` python
def computer_sample():
    """
    Profile for HP Pavilion G Series
    """
    env.hostname = 'virtualbox'
    env.locale = 'fr_FR.UTF-8'
    env.keymap = 'fr-pc'
    env.timezone_continent = 'Europe'
    env.timezone_city = 'City'
    env.arch = 'x86_64'
    env.disk = '/dev/sda'
    env.part = {
        '/': {'device': '/dev/sda3', 'ptype': 'Linux', 'ftype': 'ext4'},
        '/boot': {'device': '/dev/sda1', 'ptype': 'Linux', 'ftype': 'ext2'},
        'swap': {'device': '/dev/sda2', 'ptype': 'Linux swap / Solaris', 'ftype': 'swap'},
    }
```
