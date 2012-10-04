from fabric.api import env

env.user = 'moacir.moda'
env.rootpath = '/home/aplicacoes/submission/'
env.path = env.rootpath + 'lilacs/'
env.gitpath = env.rootpath + 'submission-git/'
env.virtualenv = env.rootpath + 'submission-env'

def test():
    env.hosts = ['ts01dx']