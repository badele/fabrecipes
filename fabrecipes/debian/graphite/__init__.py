# Library

# Fabric
from fabric.api import settings, task, sudo, env, run
from fabric.operations import put
from fabric.api import cd

# Fabtools
from fabtools import service
from fabtools import require


"""
   Install graphite stack
"""


@task
def install():
    """
    Install graphite stack
    """

    # Requirement platform
    require.deb.packages([
        'gcc',
        'python-dev',
        'python-pip'
    ])

    # Install Graphite
    run('mkdir -p /opt/graphite')
    run('pip install whisper carbon graphite-web')

    # Prepare Carbon
    with cd('/opt/graphite/conf/'):
        run('cp carbon.conf.example carbon.conf')
        run('cp storage-schemas.conf.example storage-schemas.conf')

    # Set initd
    put('files/carbon', '/etc/init.d/', mode=0755)
    run('update-rc.d carbon defaults')
    service.start('carbon')

    # Install Django
    run ('pip install django django-tagging')

    with cd('/opt/graphite/webapp/graphite'):
        run ('cp local_settings.py.example local_settings.py')
        put('files/local_settings.py', '/opt/graphite/webapps/graphite/')
        run('python manage.py syncdb')
        run('python manage.py runserver')