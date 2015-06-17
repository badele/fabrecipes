
# Fabric
from fabric.api import settings, hide, task, sudo, env, run, abort
from fabric.colors import red

# Fabtools
from fabtools import files
from fabtools import network
from fabtools import service
from fabtools import ovswitch
from fabtools.utils import run_as_root
from fabtools import require


@task
def require_docker():
    """
    Install a docker core
    """

    # Install package
    if not files.exists('/usr/bin/docker'):
        require.deb.update_index()
        require.docker.core()

    # Requirement platform
    require.deb.packages([
        'openvswitch-switch'
    ])

    # Group user
    if env.user != 'root':
        require.user(env.user, group='docker')

    require.service.started('docker')

@task
def install():
    """
    Before use it, must do
    apt-get install sudo
    adduser username sudo
    add new network card
    dhclient eth1
    """

    # Management card address
    mgtmacaddress = 'a6:88:fe:f0:d5:2d'
    vswitchname = "vswitch0"
    vswitchport = "eth0"

    # Check if we use the management interface
    (user, ip) = env.host_string.split("@")
    ismanagement = False
    print network
    for interface in network.interfaces():
        if interface != 'lo':
            if network.mac(interface) == mgtmacaddress:
                ismanagement = True
                break

    # Require docker
    require_docker()

    if not ismanagement:
        raise Exception('Please use the management network card with %(mgtmacaddress)s MAC address' % locals())

    # Configure networks
    require.file('/etc/network/interfaces', source='interfaces', use_sudo=True)
    service.reload('networking')

    # Add open vSwitch
    bridges = ovswitch.bridges()
    if vswitchname not in bridges:
        ovswitch.add_bridge(vswitchname)
        ovswitch.add_port2bridge(vswitchport,vswitchname)
        print(red("Plese reboot your system"))
