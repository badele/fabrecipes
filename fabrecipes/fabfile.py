# Fabric
from fabric.api import env, task, run, shell_env
from fabtools import system

# Fabrecipes
import archlinux
from fabrecipes import computer
from fabrecipes.commons import dotfiles


@task
def capabilities():
    """Test capabilities functions in new distrition
    For openwrt:
      mv /etc/banner /etc/banner.disable
      fab -s "/bin/sh -l -c" capabilities
    """

    print ("SYSTEM")
    print ("======")
    print("Distribution: %s" % system.distrib_id())
    print("Release: %s" % system.distrib_release())
    print("Codename: %s" % system.distrib_codename())
    print("Desc: %s" % system.distrib_desc())
    print("Arch: %s" % system.get_arch())
    print("Hostname: %s" % system.get_hostname())
