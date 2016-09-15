import requests
from fabric.api import task, local, abort
from pathlib import Path
from Deploy.config import (CUT_TO, CUT_FROM, CHOWN_CMD, GITHUB_API_URL,
                           GITHUB_PUSH_CMD, MK_VENV, SET_VENVPROJECT, PIP_INSTALL_REQ,
                           DJANGO_STARTPROJECT, WORKON_VENV,
                           SETTINGS_PY, SETTINGS_TXT, GITHUB_DATA_JSON, CD)

def cmd(command):
    "wrapper around local to use zsh"
    local(command, shell='/bin/zsh')

def _setup_venv():
    "create venv and link it to project"
    cmd(MK_VENV)
    cmd(SET_VENVPROJECT)

def _edit_settings():
    "change database settings in settings.py"
    with SETTINGS_PY.open() as fpr:
        settings_py = fpr.readlines()
    line_from = settings_py.index(CUT_FROM)
    first = settings_py[:line_from]
    lines_to_cut = settings_py[line_from:].index(CUT_TO)
    last = settings_py[line_from+lines_to_cut:]
    with SETTINGS_TXT.open() as fpr:
        middle = fpr.readlines()
    whole_file = first + middle + last
    with SETTINGS_PY.open('w') as fpr:
        fpr.write(''.join(whole_file))

@task
def deploy_dev():
    _setup_venv()
    cmd(PIP_INSTALL_REQ)
    cmd(DJANGO_STARTPROJECT)
    cmd(CHOWN_CMD)
    _edit_settings()

@task
def git_init():
    # .git may be from cloning deployment code
    # must be replaced with .git of project code
    if Path('.git').exists():
        cmd('rm -rf .git')
    cmd("git init && git add . && git commit -m 'first commit'")
    response = requests.post(GITHUB_API_URL, data=GITHUB_DATA_JSON)
    if response.status_code != 201:
        abort("Request to create repos failed!")
    cmd(GITHUB_PUSH_CMD)

@task
def up():
    cmd(CD + 'docker-compose up')

@task
def down(command=None):
    stop_cmd = CD + 'docker-compose down'
    if command:
        cmd(stop_cmd + ' && ' + command)
    else:
        cmd(stop_cmd)


def _pip(command):
    pkg = input('Package to %s: ' % command)
    cmd(WORKON_VENV + ('pip %s ' % command) + pkg)
    cmd(WORKON_VENV + 'pip freeze > requirements.txt')
    down('docker-compose build')

@task
def pip_install():
    _pip('install')

@task
def pip_uninstall():
    _pip('unistall')
