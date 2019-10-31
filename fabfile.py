from fabric.api import env, local, cd, run, task
from prettyconf import config

env.hosts = config('DEPLOY_MACHINES', cast=config.list)


@task
def deploy():
    local('git push')
    with cd('~/pylique'):
        run('git pull')
        run('pipenv install --skip-lock')
        run('supervisorctl restart pylique')
