# StoryMaker Mezzanine Development

## 1. Setup project

```
$ pip install -r ./mezzanine/project_template/requirements.txt
(Note you must run pip install -r from this directory due to pip local directory dependency issues: https://github.com/pypa/pip/issues/328)
$ cp mezzanine/project_template/local_settings.py{.template,}
$ cp mezzanine/project_template/dev.db{.default,}
$ python setup.py develop
```
[Ed: ~~`$ pip install git+https://github.com/glassresistor/django-oauth2-provider.git`~~
(Branch of provider that supports Django 1.7;  Now included in requirements.txt.)]

## 2. Create Superuser

```
python mezzanine/project_template/manage.py createsuperuser
```

## 3. Run server

```
$ python mezzanine/project_template/manage.py runserver
```

## Migrations

Whenever you alter the model run the following before committing:

```
$ python mezzanine/project_template/manage.py makemigrations
```

Then to apply those migrations to your local database:

```
$ python mezzanine/project_template/manage.py migrate

```

See [Django Docs]($ python mezzanine/project_template/manage.py makemigrations) for more info.

# Production DRAFT v0.0

## Context

Our current configuration roughly follows the uwsgi tutorial for [Django and nginx](http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html).

- nginx
    - via `/etc/nginx/conf.d/default.conf`
    - socket connection to uwsgi
- uwsgi
    - manage with emperor (loaded via `/etc/rc.local`)
- virtualenv
- debian (7/wheezy)

Logs are in the usual places for Debian (e.g. `/var/log/nginx/error.log`) and /[deploy_user]/logs/ - check timestamps if unsure. Ripe for improvement.

## Deploying to production

*Do not rely on this guide.*

### Prerequisites

- cert access to production's deploy user
- access to repo

### Process

0. USE THE BUDDY SYSTEM
0. REVIEW THE FULL CHANGE/COMMIT LOG
0. TEST AGAIN (if test and production diverge, you are not testing)
0. SCHEDULE THE DEPLOY
0. ssh to production using deploy credential
0. `tmux a -t deploy` or `tmux new -s deploy`; don't let a disconnect get you down
    0. if new tmux session: `/bin/bash` to make your life easier (do not change the default shell)
    0. if new tmux session: `cd venv/mezzanine/`
0. `git fetch && git status` and check carefully for weirdness, branch, etc.
0. `git pull origin [branchname]`
0. `mezzanine/project_template/manage.py migrate`
0. `touch mezzanine/project_template/uwsgi.ini`
