import random

from dotenv import load_dotenv
from fabric.api import cd, env, local, run
from fabric.contrib.files import append, exists

REPO_URL = 'https://github.com/paveldroo/tdd_webapp.git'


def deploy():
    site_folder = f'/var/www/{env.host}'
    run(f'sudo mkdir -p {site_folder} && sudo chown -R $(whoami):$(whoami) {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not exists('.venv/bin/pip'):
        run(f'python3.8 -m venv .venv')
    run('./.venv/bin/pip install -r requirements.txt')


def _create_or_update_dotenv():
    load_dotenv('.env')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if 'SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'SECRET_KEY={new_secret}')


def _update_static_files():
    run('./.venv/bin/python manage.py collectstatic --noinput')


def _update_database():
    run('./.venv/bin/python manage.py migrate --noinput')
