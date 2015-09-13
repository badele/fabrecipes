# Library
import re

# Fabric
from fabric.api import settings, hide, task, sudo, env, run, abort
from fabric.colors import red

# Fabtools
from fabtools import files
from fabtools import service
from fabtools import require
from fabtools.files import is_link
from fabtools.utils import run_as_root
from fabtools.require.files import template_file

"""
   Hosting tools

   Deploy example:

   fab --host root@192.168.253.35 install:hostdir=/data/backup/hosting
   fab --host root@192.168.253.35 addWebserver:webserver=domotique
   fab --host root@192.168.253.35 addRootFlask:webserver=domotique,appname=serialkiller
"""


@task
def install(hostdir):
    """
    Prepare nginx hosting server
    """

    # Install package
    require.deb.packages([
        'rsync',
        'curl',
        'sudo',
        'uwsgi',
        'uwsgi-plugin-python'
    ])
    require.python.pip()
    # require.python.packages([
    #     'uwsgi'
    # ])
    require.nginx.server()

    # Install default server
    docroot = hostdir
    server_name = "default"
    createDirectory(hostdir, server_name)
    run('cp /usr/share/nginx/www/* %(docroot)s/%(server_name)s/www' % locals())
    require.nginx.disabled('default')

    CONFIG_TPL = '''
    server {
        listen      %(port)d;
        server_name %(server_name)s %(server_alias)s;
        root        %(docroot)s/%(server_name)s/www;
        access_log  %(docroot)s/%(server_name)s/log/access.log;
    }'''

    require.nginx.site(
        'default', template_contents=CONFIG_TPL,
        port=80,
        server_alias='localhost',
        docroot=hostdir,
    )


@task
def addWebserver(webserver):
    """
    Add a virtual webserver
    :param webserver:
    :return:
    """
    hostdir = gethostdir()

    # Stop uwsgi
    service.stop('uwsgi')

    # Create user
    homedir = '%(hostdir)s/%(webserver)s' % locals()
    require.user(webserver, home=homedir, shell='/bin/bash',)

    # Create web directory
    createDirectory(hostdir, webserver)

    CONFIG_TPL = '''
    server {
        server_name %(server_name)s %(server_alias)s;
        root        %(docroot)s/%(server_name)s/www;
        access_log  %(docroot)s/%(server_name)s/log/access.log;
    }'''

    require.nginx.site(
        webserver, template_contents=CONFIG_TPL,
        server_alias='',
        docroot=hostdir,
    )

    require.network.host('127.0.0.1', webserver)


@task
def addRootFlask(webserver, appname):
    """
    Add a flask webserver
    :param webserver:
    :param appname:
    :return:
    """
    hostdir = gethostdir()

    # Create web directory
    createDirectory(hostdir, webserver)

    # Add a nginx
    CONFIG_TPL = '''
    server {
        server_name %(server_name)s %(server_alias)s;
        root        %(docroot)s/%(server_name)s/www;
        access_log  %(docroot)s/%(server_name)s/log/access.log;
        error_log  %(docroot)s/%(server_name)s/log/error.log;

        location / { try_files $uri @%(appname)s; }
        location @%(appname)s {
            include uwsgi_params;
            uwsgi_pass unix:/run/uwsgi/app/%(server_name)s_%(appname)s/socket;
        }

    }'''

    require.nginx.site(
        webserver, template_contents=CONFIG_TPL,
        appname=appname,
        server_alias='',
        docroot=hostdir,
    )

    # Add a uwsgi
    config_filename = '/etc/uwsgi/apps-available/%(webserver)s_%(appname)s.ini' % locals()



    CONFIG_TPL = '''
    [uwsgi]
    uid = %(server_name)s
    gid = %(server_name)s
    callable = app
    plugins = python

    base = %(hostdir)s/%(server_name)s/www
    pythonpath = %(hostdir)s/%(server_name)s/www/%(appname)s
    virtualenv = %(hostdir)s/%(server_name)s/venv
    wsgi-file = /data/backup/hosting/domotique/www/%(appname)s/sk_server.py
    env = %(APPNAME)s_SETTINGS=/data/backup/hosting/domotique/conf/%(appname)s.cfg

    logto = /var/log/uwsgi/%(server_name)s_%(appname)s.log
    chmod-socket = 666

    # Optional
    emperor = /tmp
    emperor-tyrant = true
    cap = setgid,setuid
    '''

    template_file(config_filename,
                  template_contents=CONFIG_TPL,
                  template_source=None,
                  context={
                      'server_name': webserver,
                      'hostdir': hostdir,
                      'appname': appname,
                      'APPNAME': appname.upper()
                  }
    )

    active_uwsgi(webserver, appname)
    service.restart('uwsgi')
    service.restart('nginx')


    require.network.host('127.0.0.1', webserver)


def gethostdir():
    hostdir = ""

    # Check if the prerequite is installed
    defaultfile = '/etc/nginx/sites-available/default.conf'
    if not files.is_file(defaultfile):
        abort(red("Please use the install before use this"))

    with settings(hide('running', 'stdout')):
        res = sudo("cat %(defaultfile)s | egrep 'root +/'" % locals())

    if 'root' in res:
        m = re.match('root +(/.*)/default/www;$', res)
        if m:
            hostdir = m.group(1)
        else:
            abort(red("not hostfile found"))

    return hostdir


def createDirectory(rootdir, webserver):

    # Log directory
    require.files.directory(
        '%(rootdir)s/%(webserver)s/conf' % locals(),
    )

    # Log directory
    require.files.directory(
        '%(rootdir)s/%(webserver)s/log' % locals(),
    )

    # Web directory
    webdirectory = '%(rootdir)s/%(webserver)s/www' % locals()
    require.files.directory(
        webdirectory,
    )

    require.python.virtualenv(
        '%(rootdir)s/%(webserver)s/venv' % locals(),
        use_sudo = True,
        user = webserver
    )

    if webserver == 'default':
        return

    chown = 'chown -R %(webserver)s:%(webserver)s %(webdirectory)s' % locals()
    run_as_root(chown)


def active_uwsgi(webserver, appname):
    config_filename = '/etc/uwsgi/apps-available/%(webserver)s_%(appname)s.ini' % locals()
    link_filename = '/etc/uwsgi/apps-enabled/%(webserver)s_%(appname)s.ini' % locals()

    if not is_link(link_filename):
        run_as_root("ln -s %(config_filename)s %(link_filename)s" % locals())
