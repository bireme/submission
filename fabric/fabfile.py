# -*- coding: utf-8 -*-
import os
from fabric.api import env, local, settings, abort, run, cd
from fabric.operations import local, put, sudo, get
from fabric.context_managers import prefix
from environment import *
 
def reset_db(app):
    """Realiza reset do app
    """    
    with prefix('. %s/bin/activate' % env.virtualenv):
        with cd(env.path):   
            run('python manage.py reset %s' % app) 
            run('python manage.py syncdb')
            run('python manage.py loaddata fixtures/%s.json' % app)    

def restart_app():
    """Restarts remote wsgi.
    """
    with cd(os.path.join(env.path,'..')):
        run("touch application.wsgi")

def update_version_file():
    with cd(env.path):
        run("git describe --tags | cut -f 1,2 -d - > templates/version.txt")
        # traz o arquivo gerado da versão para minha máquina, e implementa a versão localmente
        get("templates/version.txt", "../lilacs_submission/templates")

def update():
    """Somente atualiza código (git pull) e restart serviço
    """
    with cd(env.gitpath):
        run("git pull")

    update_version_file()
    restart_app()
