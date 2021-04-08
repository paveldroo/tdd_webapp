import random

from django.conf import settings
from dotenv import load_dotenv
from fabric.api import cd, env, local, run
from fabric.context_managers import prefix
from fabric.contrib.files import append, exists

REPO_URL = 'https://github.com/paveldroo/tdd_webapp.git'
VENV_ACTIVATION_PREFIX = 'source .venv/bin/activate'


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
    with prefix(VENV_ACTIVATION_PREFIX):
        run('pip install -r requirements.txt')


def _create_or_update_dotenv():
    load_dotenv(settings.BASE_DIR / '.env')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if 'SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'SECRET_KEY={new_secret}')


def _update_static_files():
    with prefix(VENV_ACTIVATION_PREFIX):
        run('./manage.py collectstatic --noinput')


def _update_database():
    with prefix(VENV_ACTIVATION_PREFIX):
        run('./manage.py migrate --noinput')
