# Library

# Fabric
from fabric.api import settings, task, sudo, env, run

# Fabtools
from fabtools import require


"""
   salt tools
"""


@task
def master():
    """
    Install salt-master
    """

    # Add salt sources.list
    require.deb.ppa('ppa:saltstack/salt')
    # require.deb.source('salt', 'http://debian.saltstack.com/debian wheezy-saltstack', 'wheezy-saltstack', 'main')

    # Install salt-master
    require.deb.packages(
        [
            'salt-master',
            'salt-cloud',
        ]
    )

