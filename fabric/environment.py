from fabric.api import env

env.user = 'moacir.moda'
env.path = '/home/aplicacoes/submission/'
env.gitpath = env.path + 'submission-git'
env.virtualenv = env.path + 'submission-env'

def test():
    env.hosts = ['ts01dx']