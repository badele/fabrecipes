# Library
import os

# Fabric
from fabric.api import settings, task, env, run, local, hide
from fabric.colors import red
from fabric.operations import put

# Fabtools
from fabtools import openwrt
from fabtools import require
from fabtools import disk

"""
OpenWrt Parental Control
"""


@task
def install():
    """
    Install a Parental Control on OpenWrt router
    """

    # Set Shell environment
    env.shell = "/bin/ash -l -c"

    # Install USB required packages
    openwrt.update_index()
    openwrt.install([
        'tinyproxy',
    ])

    print ("Set configuration")

    with settings(hide('running', 'warnings', 'stdout')):
        run('mkdir -p /var/etc/tinyproxy')
        run('echo "youporn" >> /var/etc/tinyproxy/filter')

        run('touch /var/log/tinyproxy.log')
        run('chown nobody:nogroup /var/log/tinyproxy.log')

    openwrt.uci_set([
        "tinyproxy.@tinyproxy[0].Allow=192.168.253.0/24",
        "tinyproxy.@tinyproxy[0].Filter=/var/etc/tinyproxy/filter",
        "tinyproxy.@tinyproxy[0].enabled=1",
        "tinyproxy.@tinyproxy[0].Syslog=0",
    ])

    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        run('/etc/init.d/tinyproxy enable')

    update()


@task
def update():
    """
    Update Parental Control with the blacklist UT1
    """

    # Set Shell environment
    env.shell = "/bin/ash -l -c"

    local('mkdir -p /tmp/tinyproxy')
    local("wget ftp://ftp.ut-capitole.fr/pub/reseau/cache/squidguard_contrib/blacklists.tar.gz -O /tmp/tinyproxy/blacklists.tar.gz")
    local('tar -xzf /tmp/tinyproxy/blacklists.tar.gz -C /tmp/tinyproxy/')

    ignores = [
        'ads',
        'drogue',
        'agressif',
    ]

    local('echo "" > /tmp/tinyproxy/filter')
    for ignore in ignores:
        local('cat /tmp/tinyproxy/blacklists/%s/domains >> /tmp/tinyproxy/filter' % ignore)

    put('/tmp/tinyproxy/filter', '/var/etc/tinyproxy/filter')

    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        #run('/etc/init.d/tinyproxy stop')
        #run('/etc/init.d/tinyproxy start')
        print(red('Please restart tinyproxy with /etc/init.d/tinyproxy restart'))
